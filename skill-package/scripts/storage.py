"""
Multi-Backend Storage System for Claude Skills
Supports: Local Filesystem, GitHub, Checkpoint, Email, Notion
"""

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path
import json

# Optional dependencies with graceful degradation
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("Warning: PyYAML not installed. Config file loading will fail.")

try:
    from github import Github
    HAS_GITHUB = True
except ImportError:
    HAS_GITHUB = False
    # Only warn if actually trying to use GitHub backend

try:
    from notion_client import Client as NotionClient
    HAS_NOTION = True
except ImportError:
    HAS_NOTION = False
    # Only warn if actually trying to use Notion backend


class StorageBackend(ABC):
    """Base class for all storage backends"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name"""
        pass
    
    @abstractmethod
    def save(self, key: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """Save content with key. Returns success status."""
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[str]:
        """Load content by key. Returns None if not found."""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass
    
    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete content by key."""
        pass
    
    def log(self, message: str) -> bool:
        """Log operation (optional, backend-specific)"""
        return self.save(f"logs/{self._timestamp()}.log", message, metadata={'type': 'log'})
    
    @staticmethod
    def _timestamp() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")


class LocalFilesystemBackend(StorageBackend):
    """Local filesystem storage via MCP"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self._ensure_dirs()
    
    @property
    def name(self) -> str:
        return "Local Filesystem"
    
    def _ensure_dirs(self):
        for subdir in ['config', 'db', 'logs']:
            (self.base_path / subdir).mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, content: str, metadata: Optional[Dict] = None) -> bool:
        try:
            file_path = self.base_path / key
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"LocalFS save error: {e}")
            return False
    
    def load(self, key: str) -> Optional[str]:
        try:
            file_path = self.base_path / key
            return file_path.read_text(encoding='utf-8') if file_path.exists() else None
        except Exception as e:
            print(f"LocalFS load error: {e}")
            return None
    
    def exists(self, key: str) -> bool:
        return (self.base_path / key).exists()
    
    def list_keys(self, prefix: str = "") -> List[str]:
        try:
            search_path = self.base_path / prefix if prefix else self.base_path
            return [str(p.relative_to(self.base_path)) for p in search_path.rglob("*") if p.is_file()]
        except Exception as e:
            print(f"LocalFS list error: {e}")
            return []
    
    def delete(self, key: str) -> bool:
        try:
            file_path = self.base_path / key
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"LocalFS delete error: {e}")
            return False


class GitHubBackend(StorageBackend):
    """GitHub repository storage"""
    
    def __init__(self, repo_name: str, token: str, branch: str = "main"):
        if not HAS_GITHUB:
            print("Error: PyGithub not installed. Run: pip install PyGithub")
            self._initialized = False
            return
        
        try:
            self.g = Github(token)
            self.repo = self.g.get_repo(repo_name)
            self.branch = branch
            self._initialized = True
        except Exception as e:
            print(f"GitHub init error: {e}")
            self._initialized = False
    
    @property
    def name(self) -> str:
        return "GitHub Repository"
    
    def save(self, key: str, content: str, metadata: Optional[Dict] = None) -> bool:
        if not self._initialized:
            return False
        
        try:
            message = metadata.get('message', f"Update {key}") if metadata else f"Update {key}"
            
            try:
                # Update existing file
                file = self.repo.get_contents(key, ref=self.branch)
                self.repo.update_file(key, message, content, file.sha, branch=self.branch)
            except:
                # Create new file
                self.repo.create_file(key, message, content, branch=self.branch)
            
            return True
        except Exception as e:
            print(f"GitHub save error: {e}")
            return False
    
    def load(self, key: str) -> Optional[str]:
        if not self._initialized:
            return None
        
        try:
            file = self.repo.get_contents(key, ref=self.branch)
            return file.decoded_content.decode('utf-8')
        except Exception as e:
            return None
    
    def exists(self, key: str) -> bool:
        return self.load(key) is not None
    
    def list_keys(self, prefix: str = "") -> List[str]:
        if not self._initialized:
            return []
        
        try:
            contents = self.repo.get_contents(prefix or "", ref=self.branch)
            keys = []
            
            def collect_files(items):
                for item in items:
                    if item.type == "file":
                        keys.append(item.path)
                    elif item.type == "dir":
                        collect_files(self.repo.get_contents(item.path, ref=self.branch))
            
            collect_files(contents if isinstance(contents, list) else [contents])
            return keys
        except Exception as e:
            return []
    
    def delete(self, key: str) -> bool:
        if not self._initialized:
            return False
        
        try:
            file = self.repo.get_contents(key, ref=self.branch)
            self.repo.delete_file(key, f"Delete {key}", file.sha, branch=self.branch)
            return True
        except Exception as e:
            return False
    
    def get_history(self, key: str, limit: int = 10) -> List[Dict]:
        """Get commit history for a file"""
        if not self._initialized:
            return []
        
        try:
            commits = self.repo.get_commits(path=key, sha=self.branch)
            return [{
                'date': str(c.commit.author.date),
                'message': c.commit.message,
                'author': c.commit.author.name,
                'sha': c.sha
            } for c in list(commits)[:limit]]
        except:
            return []


class CheckpointBackend(StorageBackend):
    """Session-only storage with export/import"""
    
    def __init__(self):
        self._data: Dict[str, str] = {}
        self._metadata: Dict[str, Dict] = {}
    
    @property
    def name(self) -> str:
        return "Checkpoint (Session Only)"
    
    def save(self, key: str, content: str, metadata: Optional[Dict] = None) -> bool:
        self._data[key] = content
        if metadata:
            self._metadata[key] = metadata
        return True
    
    def load(self, key: str) -> Optional[str]:
        return self._data.get(key)
    
    def exists(self, key: str) -> bool:
        return key in self._data
    
    def list_keys(self, prefix: str = "") -> List[str]:
        if not prefix:
            return list(self._data.keys())
        return [k for k in self._data.keys() if k.startswith(prefix)]
    
    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            self._metadata.pop(key, None)
            return True
        return False
    
    def export_checkpoint(self) -> Dict[str, Any]:
        """Export all data as checkpoint"""
        from datetime import datetime
        return {
            'version': '1.0',
            'timestamp': datetime.now().isoformat(),
            'backend': 'checkpoint',
            'data': self._data.copy(),
            'metadata': self._metadata.copy()
        }
    
    def import_checkpoint(self, checkpoint: Dict[str, Any]) -> bool:
        """Import checkpoint data"""
        try:
            self._data = checkpoint.get('data', {})
            self._metadata = checkpoint.get('metadata', {})
            return True
        except Exception as e:
            print(f"Checkpoint import error: {e}")
            return False


class EmailBackend(StorageBackend):
    """Email-based storage"""
    
    def __init__(self, imap_server: str, smtp_server: str, email: str, 
                 password: str, folder: str = "Claude/SkillData"):
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
        self.folder = folder
        self._initialized = self._test_connection()
    
    @property
    def name(self) -> str:
        return "Email Storage"
    
    def _test_connection(self) -> bool:
        try:
            import imaplib
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email, self.password)
            mail.logout()
            return True
        except Exception as e:
            print(f"Email connection error: {e}")
            return False
    
    def save(self, key: str, content: str, metadata: Optional[Dict] = None) -> bool:
        if not self._initialized:
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = f"[Claude Skill Data] {key}"
            
            body = f"Key: {key}\nTimestamp: {self._timestamp()}\n\n{content}"
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
                server.login(self.email, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email save error: {e}")
            return False
    
    def load(self, key: str) -> Optional[str]:
        if not self._initialized:
            return None
        
        try:
            import imaplib
            import email as email_lib
            
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email, self.password)
            mail.select(self.folder)
            
            # Search for emails with this key in subject
            search_criteria = f'(SUBJECT "[Claude Skill Data] {key}")'
            _, messages = mail.search(None, search_criteria)
            
            if messages[0]:
                # Get most recent
                latest_id = messages[0].split()[-1]
                _, msg_data = mail.fetch(latest_id, '(RFC822)')
                
                email_body = msg_data[0][1]
                email_message = email_lib.message_from_bytes(email_body)
                
                # Extract content
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True).decode()
                            # Extract actual content (after metadata lines)
                            lines = payload.split('\n')
                            content_start = next((i for i, line in enumerate(lines) if line.strip() == ''), 2) + 1
                            mail.logout()
                            return '\n'.join(lines[content_start:])
                
            mail.logout()
            return None
        except Exception as e:
            print(f"Email load error: {e}")
            return None
    
    def exists(self, key: str) -> bool:
        return self.load(key) is not None
    
    def list_keys(self, prefix: str = "") -> List[str]:
        # Email backend lists by searching subjects
        return []  # Simplified - would need full email parsing
    
    def delete(self, key: str) -> bool:
        # Email deletion is complex - mark as deleted or move to trash
        return False  # Simplified - emails typically archived, not deleted


class NotionBackend(StorageBackend):
    """Notion database storage"""
    
    def __init__(self, token: str, database_id: str):
        if not HAS_NOTION:
            print("Error: notion-client not installed. Run: pip install notion-client")
            self._initialized = False
            return
        
        try:
            self.client = NotionClient(auth=token)
            self.database_id = database_id
            self._initialized = True
        except Exception as e:
            print(f"Notion init error: {e}")
            self._initialized = False
    
    @property
    def name(self) -> str:
        return "Notion Database"
    
    def save(self, key: str, content: str, metadata: Optional[Dict] = None) -> bool:
        if not self._initialized:
            return False
        
        try:
            # Check if page exists
            existing = self._find_page(key)
            
            properties = {
                "Name": {"title": [{"text": {"content": key}}]},
                "Content": {"rich_text": [{"text": {"content": content[:2000]}}]},  # Notion limit
                "Updated": {"date": {"start": self._get_iso_timestamp()}}
            }
            
            if existing:
                # Update existing
                self.client.pages.update(page_id=existing['id'], properties=properties)
            else:
                # Create new
                self.client.pages.create(
                    parent={"database_id": self.database_id},
                    properties=properties
                )
            
            return True
        except Exception as e:
            print(f"Notion save error: {e}")
            return False
    
    def load(self, key: str) -> Optional[str]:
        if not self._initialized:
            return None
        
        try:
            page = self._find_page(key)
            if page:
                # Get content from page properties
                content_prop = page.get('properties', {}).get('Content', {})
                rich_text = content_prop.get('rich_text', [])
                if rich_text:
                    return rich_text[0].get('text', {}).get('content', '')
            return None
        except Exception as e:
            return None
    
    def exists(self, key: str) -> bool:
        return self._find_page(key) is not None
    
    def list_keys(self, prefix: str = "") -> List[str]:
        if not self._initialized:
            return []
        
        try:
            results = self.client.databases.query(database_id=self.database_id)
            keys = []
            for page in results.get('results', []):
                title_prop = page.get('properties', {}).get('Name', {}).get('title', [])
                if title_prop:
                    key = title_prop[0].get('text', {}).get('content', '')
                    if not prefix or key.startswith(prefix):
                        keys.append(key)
            return keys
        except Exception as e:
            return []
    
    def delete(self, key: str) -> bool:
        if not self._initialized:
            return False
        
        try:
            page = self._find_page(key)
            if page:
                self.client.pages.update(page_id=page['id'], archived=True)
                return True
            return False
        except Exception as e:
            return False
    
    def _find_page(self, key: str) -> Optional[Dict]:
        """Find page by key (name)"""
        try:
            results = self.client.databases.query(
                database_id=self.database_id,
                filter={"property": "Name", "title": {"equals": key}}
            )
            return results.get('results', [None])[0]
        except:
            return None

    def _get_iso_timestamp(self) -> str:
        """Get ISO 8601 formatted timestamp for Notion"""
        from datetime import datetime
        return datetime.now().isoformat()


# Storage Manager - handles backend selection and initialization

class StorageManager:
    """Manages storage backend selection and operations"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.backend: Optional[StorageBackend] = None
        self.config = self._load_config(config_path) if config_path else {}
        
        if self.config:
            self._initialize_from_config()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load storage configuration"""
        if not HAS_YAML:
            print("Error: PyYAML required for config file loading")
            return {}
        
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Config load error: {e}")
            return {}
    
    def _initialize_from_config(self):
        """Initialize backend from config"""
        backend_type = self.config.get('storage', {}).get('backend')
        
        if backend_type == 'local':
            self.use_local_filesystem(self.config['storage']['local']['base_path'])
        elif backend_type == 'github':
            gh = self.config['storage']['github']
            self.use_github(gh['repo'], gh['token'], gh.get('branch', 'main'))
        elif backend_type == 'checkpoint':
            self.use_checkpoint()
        elif backend_type == 'email':
            em = self.config['storage']['email']
            self.use_email(em['imap_server'], em['smtp_server'], em['email'], 
                          em['password'], em.get('folder', 'Claude/SkillData'))
        elif backend_type == 'notion':
            nt = self.config['storage']['notion']
            self.use_notion(nt['token'], nt['database_id'])
    
    def use_local_filesystem(self, base_path: str):
        """Switch to local filesystem backend"""
        self.backend = LocalFilesystemBackend(base_path)
        print(f"✅ Using: {self.backend.name}")
    
    def use_github(self, repo: str, token: str, branch: str = "main"):
        """Switch to GitHub backend"""
        self.backend = GitHubBackend(repo, token, branch)
        print(f"✅ Using: {self.backend.name}")
    
    def use_checkpoint(self):
        """Switch to checkpoint backend"""
        self.backend = CheckpointBackend()
        print(f"✅ Using: {self.backend.name}")
    
    def use_email(self, imap: str, smtp: str, email: str, password: str, folder: str):
        """Switch to email backend"""
        self.backend = EmailBackend(imap, smtp, email, password, folder)
        print(f"✅ Using: {self.backend.name}")
    
    def use_notion(self, token: str, database_id: str):
        """Switch to Notion backend"""
        self.backend = NotionBackend(token, database_id)
        print(f"✅ Using: {self.backend.name}")
    
    def get_backend_name(self) -> str:
        """Get current backend name"""
        return self.backend.name if self.backend else "None"
    
    # Proxy methods to current backend
    
    def save(self, key: str, content: str, **kwargs) -> bool:
        if not self.backend:
            raise RuntimeError("No storage backend initialized")
        return self.backend.save(key, content, kwargs.get('metadata'))
    
    def load(self, key: str) -> Optional[str]:
        if not self.backend:
            raise RuntimeError("No storage backend initialized")
        return self.backend.load(key)
    
    def exists(self, key: str) -> bool:
        if not self.backend:
            return False
        return self.backend.exists(key)
    
    def list_keys(self, prefix: str = "") -> List[str]:
        if not self.backend:
            return []
        return self.backend.list_keys(prefix)
    
    def delete(self, key: str) -> bool:
        if not self.backend:
            return False
        return self.backend.delete(key)


# Global instance
_storage: Optional[StorageManager] = None


def init_storage(config_path: Optional[str] = None) -> StorageManager:
    """Initialize global storage manager"""
    global _storage
    _storage = StorageManager(config_path)
    return _storage


def get_storage() -> StorageManager:
    """Get global storage manager"""
    if _storage is None:
        raise RuntimeError("Storage not initialized. Call init_storage() first.")
    return _storage


# Convenience functions

def save_data(key: str, content: str, **kwargs) -> bool:
    """Save data using current backend"""
    return get_storage().save(key, content, **kwargs)


def load_data(key: str) -> Optional[str]:
    """Load data using current backend"""
    return get_storage().load(key)


def data_exists(key: str) -> bool:
    """Check if data exists"""
    return get_storage().exists(key)


def list_data(prefix: str = "") -> List[str]:
    """List data keys"""
    return get_storage().list_keys(prefix)


def delete_data(key: str) -> bool:
    """Delete data"""
    return get_storage().delete(key)
