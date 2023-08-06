from .views import (
    PostgresMaterialisedViewMixin,
    PostgresViewFromQueryset,
    PostgresViewFromSQL,
    UndocumentedPostgresViewFromQueryset,
    UndocumentedPostgresViewFromSQL,
)

from .sync import sync_views

default_app_config = 'django_views.apps.DjangoPostgresViewsConfig'
