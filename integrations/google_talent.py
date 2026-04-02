# Google Talent Solution adapter
import logging
from typing import Dict, List, Optional, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

from .base import JobBoardInterface

logger = logging.getLogger(__name__)

class GoogleTalentAdapter(JobBoardInterface):
    """
    Adapter for Google Cloud Talent Solution v4 API.
    Requires a service account with proper permissions.
    """

    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_TALENT_CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/jobs']
        )
        self.service = build('jobs', 'v4', credentials=self.credentials)
        self.project_id = f"projects/{settings.GOOGLE_CLOUD_PROJECT}"
        self.tenant_id = settings.GOOGLE_TALENT_TENANT_ID  # Optional, but recommended
        if self.tenant_id:
            self.parent = f"{self.project_id}/tenants/{self.tenant_id}"
        else:
            self.parent = self.project_id

    def _build_request(self, query: str, location: Optional[str],
                       filters: Optional[Dict]) -> Dict:
        """Construct the search request body."""
        request = {
            'query': query,
            'page_size': 20,  # Adjust as needed
        }
        if location:
            request['job_query'] = {
                'location_filters': [{'address': location}]
            }
        if filters:
            # Map filters to Google's expected format (custom attributes, etc.)
            if 'employment_types' in filters:
                request['job_query']['employment_types'] = filters['employment_types']
            if 'company_display_names' in filters:
                request['job_query']['company_display_names'] = filters['company_display_names']
            if 'custom_attributes_filter' in filters:
                request['custom_attributes_filter'] = filters['custom_attributes_filter']
        return request

    def search_jobs(self, query: str, location: Optional[str] = None,
                    filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search jobs via the v4 `projects.tenants.jobs.search` endpoint.
        Returns a list of job dictionaries.
        """
        body = self._build_request(query, location, filters)
        try:
            response = self.service.projects().tenants().jobs().search(
                parent=self.parent,
                body=body
            ).execute()
            return response.get('matchingJobs', [])
        except Exception as e:
            logger.error(f"Google Talent search failed: {e}")
            return []

    def get_job(self, job_id: str) -> Dict:
        """
        Retrieve a single job via `projects.tenants.jobs.get`.
        `job_id` is the full resource name, e.g., "projects/.../jobs/123".
        """
        try:
            response = self.service.projects().tenants().jobs().get(
                name=job_id
            ).execute()
            return response
        except Exception as e:
            logger.error(f"Google Talent get job failed: {e}")
            return {}

    def list_jobs(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        List jobs via `projects.tenants.jobs.list`.
        Supports filtering by company, etc.
        """
        request = {}
        if filters:
            # Google supports filter string like "companyName=... AND customAttributes..."
            request['filter'] = self._build_filter_string(filters)
        try:
            response = self.service.projects().tenants().jobs().list(
                parent=self.parent,
                **request
            ).execute()
            return response.get('jobs', [])
        except Exception as e:
            logger.error(f"Google Talent list jobs failed: {e}")
            return []

    def complete_query(self, query: str) -> List[str]:
        """
        Autocomplete search suggestions via `projects.tenants.completeQuery`.
        Returns a list of suggestion strings.
        """
        try:
            response = self.service.projects().tenants().completeQuery(
                name=self.parent,
                query=query,
                pageSize=10
            ).execute()
            suggestions = response.get('completionResults', [])
            return [s['suggestion'] for s in suggestions]
        except Exception as e:
            logger.error(f"Google Talent autocomplete failed: {e}")
            return []

    def create_client_event(self, event_type: str, job_id: Optional[str] = None,
                            **kwargs) -> Dict:
        """
        Track a client event via `projects.tenants.clientEvents.create`.
        event_type: e.g., "VIEW", "APPLY", "CLICK".
        job_id: the job resource name (if applicable).
        Extra kwargs can include request_id, event_notes, etc.
        """
        event = {
            'eventId': self._generate_event_id(),
            'eventType': event_type,
            'createTime': self._now_rfc3339(),
        }
        if job_id:
            event['jobEvent'] = {'jobs': [job_id]}
        # Add any extra fields from kwargs (e.g., eventNotes, requestId)
        event.update(kwargs)

        try:
            response = self.service.projects().tenants().clientEvents().create(
                parent=self.parent,
                body={'clientEvent': event}
            ).execute()
            return response
        except Exception as e:
            logger.error(f"Google Talent create client event failed: {e}")
            return {}

    def _build_filter_string(self, filters: Dict) -> str:
        """Convert a dict of filters to Google's filter string format."""
        # Example: {"companyName": "projects/.../companies/123"} -> "companyName = ..."
        clauses = []
        for key, value in filters.items():
            if isinstance(value, str):
                clauses.append(f"{key} = {value}")
            elif isinstance(value, list):
                # For IN clauses: key IN (val1, val2)
                vals = ', '.join([f"'{v}'" for v in value])
                clauses.append(f"{key} IN ({vals})")
            # Add other types as needed
        return ' AND '.join(clauses)

    def _generate_event_id(self) -> str:
        """Generate a unique event ID (could use UUID)."""
        import uuid
        return str(uuid.uuid4())

    def _now_rfc3339(self) -> str:
        """Return current UTC time in RFC 3339 format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat(timespec='seconds')
    
    def create_job(self, job_data):
        """
        job_data should be a dict with required fields as per Google API.
        """
        try:
            response = self.service.projects().tenants().jobs().create(
                parent=self.parent,
                body={'job': job_data}
            ).execute()
            return response
        except Exception as e:
            logger.error(f"Failed to create job in Google: {e}")
            raise