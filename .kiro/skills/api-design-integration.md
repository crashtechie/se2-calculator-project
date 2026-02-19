# API Design & Integration

## When to Activate This Skill

- Designing RESTful APIs or GraphQL endpoints
- Integrating with external APIs
- Building API clients or wrappers
- Implementing API authentication and authorization
- Versioning APIs or handling breaking changes
- Serializing complex Django models

## RESTful API Design Principles

### Resource-Oriented Design
```python
# Good: Resource-based URLs
/api/v1/blocks/
/api/v1/blocks/{id}/
/api/v1/blocks/{id}/components/

# Bad: Action-based URLs
/api/v1/get-blocks/
/api/v1/create-block/
```

### HTTP Methods
- GET: Retrieve resources (idempotent, cacheable)
- POST: Create new resources
- PUT: Replace entire resource
- PATCH: Partial update
- DELETE: Remove resource

### Status Codes
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Invalid input
- 401 Unauthorized: Authentication required
- 403 Forbidden: Authenticated but not authorized
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Resource conflict (e.g., duplicate)
- 422 Unprocessable Entity: Validation errors
- 500 Internal Server Error: Server-side error

## Django REST Framework Patterns

### Serializers
```python
from rest_framework import serializers
from .models import Block, Component

class ComponentSerializer(serializers.ModelSerializer):
    """Serialize component with validation"""
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'mass', 'volume', 'materials']
        read_only_fields = ['id']
    
    def validate_mass(self, value):
        """Custom field validation"""
        if value <= 0:
            raise serializers.ValidationError("Mass must be positive")
        return value

class BlockSerializer(serializers.ModelSerializer):
    """Nested serializer for related objects"""
    components = ComponentSerializer(many=True, read_only=True)
    component_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Block
        fields = ['id', 'name', 'components', 'component_count', 'created_at']
    
    def get_component_count(self, obj):
        """Computed field"""
        return obj.components.count()
```

### ViewSets
```python
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class BlockViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Block CRUD operations
    
    list: GET /api/blocks/
    create: POST /api/blocks/
    retrieve: GET /api/blocks/{id}/
    update: PUT /api/blocks/{id}/
    partial_update: PATCH /api/blocks/{id}/
    destroy: DELETE /api/blocks/{id}/
    """
    queryset = Block.objects.select_related('component').prefetch_related('materials')
    serializer_class = BlockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'component']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        """Optimize queries and filter by user"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_public=True)
        return queryset
    
    @action(detail=True, methods=['post'])
    def calculate_resources(self, request, pk=None):
        """Custom action: POST /api/blocks/{id}/calculate_resources/"""
        block = self.get_object()
        quantity = request.data.get('quantity', 1)
        resources = block.calculate_total_resources(quantity)
        return Response({'resources': resources})
```

### URL Configuration
```python
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'blocks', BlockViewSet, basename='block')
router.register(r'components', ComponentViewSet, basename='component')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

## API Versioning Strategies

### URL Path Versioning (Recommended)
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}

# urls.py
urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
]
```

### Header Versioning
```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}

# Client sends: Accept: application/json; version=1.0
```

### Handling Breaking Changes
- Deprecate old endpoints with warnings
- Maintain backward compatibility for at least 2 versions
- Document migration guides
- Use feature flags for gradual rollout

## Authentication & Authorization

### Token Authentication
```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class BlockViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

### Custom Permissions
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow owners to edit, others to read"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

### JWT Authentication
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

## Pagination

### Configuring Pagination
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### Custom Pagination
```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlockViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
```

## Error Handling

### Custom Exception Handler
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """Standardize error responses"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'error': {
                'status_code': response.status_code,
                'message': str(exc),
                'details': response.data
            }
        }
        response.data = custom_response
    
    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler'
}
```

### Validation Errors
```python
from rest_framework import serializers

class BlockSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """Cross-field validation"""
        if data.get('input_mass', 0) > data.get('output_mass', 0):
            raise serializers.ValidationError({
                'input_mass': 'Input mass cannot exceed output mass'
            })
        return data
```

## External API Integration

### Using requests Library
```python
import requests
from django.conf import settings
from typing import Dict, Any

class ExternalAPIClient:
    """Client for external API integration"""
    
    def __init__(self):
        self.base_url = settings.EXTERNAL_API_URL
        self.api_key = settings.EXTERNAL_API_KEY
        self.timeout = 30
    
    def _get_headers(self) -> Dict[str, str]:
        """Common headers for all requests"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'SE2Calculator/1.0'
        }
    
    def get_resource(self, resource_id: str) -> Dict[str, Any]:
        """Fetch resource from external API"""
        url = f'{self.base_url}/resources/{resource_id}'
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise APITimeoutError(f'Request to {url} timed out')
        except requests.exceptions.HTTPError as e:
            raise APIError(f'HTTP error: {e.response.status_code}')
        except requests.exceptions.RequestException as e:
            raise APIError(f'Request failed: {str(e)}')
```

### Async API Calls
```python
import httpx
from asgiref.sync import sync_to_async

class AsyncAPIClient:
    """Async client for better performance"""
    
    async def fetch_multiple_resources(self, resource_ids: list) -> list:
        """Fetch multiple resources concurrently"""
        async with httpx.AsyncClient() as client:
            tasks = [
                self._fetch_one(client, rid) 
                for rid in resource_ids
            ]
            return await asyncio.gather(*tasks)
    
    async def _fetch_one(self, client, resource_id):
        """Fetch single resource"""
        url = f'{self.base_url}/resources/{resource_id}'
        response = await client.get(url, headers=self._get_headers())
        return response.json()
```

### Caching API Responses
```python
from django.core.cache import cache
from functools import wraps

def cache_api_response(timeout=300):
    """Decorator to cache API responses"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f'api_{func.__name__}_{args}_{kwargs}'
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator

@cache_api_response(timeout=600)
def get_external_data(resource_id):
    """Cached API call"""
    return api_client.get_resource(resource_id)
```

## Rate Limiting

### Django REST Framework Throttling
```python
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstRateThrottle(UserRateThrottle):
    rate = '60/min'

class SustainedRateThrottle(UserRateThrottle):
    rate = '1000/day'

class BlockViewSet(viewsets.ModelViewSet):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
```

### Custom Throttle
```python
from rest_framework.throttling import SimpleRateThrottle

class IPBasedThrottle(SimpleRateThrottle):
    """Throttle by IP address"""
    scope = 'ip'
    
    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }
```

## API Documentation

### OpenAPI/Swagger with drf-spectacular
```python
# settings.py
INSTALLED_APPS = [
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Space Engineers 2 Calculator API',
    'DESCRIPTION': 'API for managing blocks, components, and build orders',
    'VERSION': '1.0.0',
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
```

### Documenting Endpoints
```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

class BlockViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary="List all blocks",
        description="Returns paginated list of blocks with optional filtering",
        parameters=[
            OpenApiParameter(
                name='name',
                description='Filter by block name',
                required=False,
                type=str
            ),
        ],
        responses={200: BlockSerializer(many=True)}
    )
    def list(self, request):
        return super().list(request)
```

## Testing APIs

### Testing ViewSets
```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class BlockAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test', 'test@example.com', 'pass')
        self.client.force_authenticate(user=self.user)
    
    def test_list_blocks(self):
        """Test GET /api/blocks/"""
        Block.objects.create(name='Test Block')
        
        response = self.client.get('/api/v1/blocks/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_block_with_valid_data(self):
        """Test POST /api/blocks/"""
        data = {'name': 'New Block', 'description': 'Test'}
        
        response = self.client.post('/api/v1/blocks/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Block.objects.filter(name='New Block').exists()
    
    def test_create_block_with_invalid_data_returns_400(self):
        """Test validation errors"""
        data = {'name': ''}  # Invalid: empty name
        
        response = self.client.post('/api/v1/blocks/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
```

### Testing External API Integration
```python
from unittest.mock import patch, Mock

def test_external_api_call_success():
    """Test successful API integration"""
    mock_response = Mock()
    mock_response.json.return_value = {'id': '123', 'name': 'Resource'}
    mock_response.status_code = 200
    
    with patch('requests.get', return_value=mock_response):
        client = ExternalAPIClient()
        result = client.get_resource('123')
        
        assert result['id'] == '123'

def test_external_api_timeout_handling():
    """Test timeout error handling"""
    with patch('requests.get', side_effect=requests.exceptions.Timeout):
        client = ExternalAPIClient()
        
        with pytest.raises(APITimeoutError):
            client.get_resource('123')
```

## Best Practices

### API Design
- Use nouns for resources, not verbs
- Keep URLs simple and intuitive
- Version your API from the start
- Use proper HTTP methods and status codes
- Provide meaningful error messages
- Document all endpoints

### Performance
- Use select_related/prefetch_related in querysets
- Implement pagination for list endpoints
- Cache expensive operations
- Use async views for I/O-bound operations
- Monitor API performance metrics

### Security
- Always use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Use authentication for sensitive endpoints
- Don't expose internal IDs if possible (use UUIDs)
- Sanitize error messages (don't leak sensitive info)

### Maintainability
- Keep serializers focused and reusable
- Use viewsets for standard CRUD operations
- Write comprehensive API tests
- Document breaking changes
- Use semantic versioning
- Maintain backward compatibility

## Common Pitfalls

### N+1 Query Problem
```python
# Bad: Causes N+1 queries
class BlockSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source='component.name')

# Good: Use select_related in viewset
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.select_related('component')
```

### Over-fetching Data
```python
# Bad: Returns all fields
class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

# Good: Explicit fields, use different serializers for list/detail
class BlockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'name', 'created_at']

class BlockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'name', 'description', 'components', 'created_at']
```

### Ignoring Validation
```python
# Bad: No validation
def create(self, request):
    Block.objects.create(**request.data)

# Good: Use serializer validation
def create(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
```

## Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [REST API Design Best Practices](https://restfulapi.net/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [HTTP Status Codes](https://httpstatuses.com/)
