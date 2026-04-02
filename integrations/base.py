# Abstract job board interface
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class JobBoardInterface(ABC):
    """Abstract base class for external job board integrations."""

    @abstractmethod
    def search_jobs(self, query: str, location: Optional[str] = None,
                    filters: Optional[Dict] = None) -> List[Dict]:
        """Search jobs with keywords and filters."""
        pass

    @abstractmethod
    def get_job(self, job_id: str) -> Dict:
        """Retrieve a single job by its external ID."""
        pass

    @abstractmethod
    def list_jobs(self, filters: Optional[Dict] = None) -> List[Dict]:
        """List jobs (for syncing/caching)."""
        pass

    @abstractmethod
    def complete_query(self, query: str) -> List[str]:
        """Autocomplete search suggestions."""
        pass

    @abstractmethod
    def create_client_event(self, event_type: str, job_id: Optional[str] = None,
                            **kwargs) -> Dict:
        """Track user interactions (views, clicks, etc.)."""
        pass