"""Module for different types of Namespaces."""

from pathlib import Path

from .models import Namespace


class DjangoApp(Namespace):
    """A class which specifies a django app."""

    def _url(self, prefix):
        """Convenience function to build urls."""
        return '{}-{}'.format(prefix, self.url)

    @property
    def url(self):
        """Return cannonical url name."""
        return '-'.join(self.app_structure[1:])

    @property
    def url_parent(self):
        """Return url parent name."""
        return '-'.join(self.app_structure[1:][:-1])

    @property
    def url_index(self):
        """Returns a url index."""
        return self._url('index')

    @property
    def url_list(self):
        """Returns a url list."""
        return self._url('list')

    @property
    def url_create(self):
        """Returns a url create."""
        return self._url('create')

    @property
    def url_detail(self):
        """Returns a url detail."""
        return self._url('detail')

    @property
    def url_update(self):
        """Returns a url update."""
        return self._url('update')

    @property
    def url_delete(self):
        """Returns a url delete."""
        return self._url('delete')

    @property
    def list_display(self):
        """Returns list_display for django admin config."""
        return [field.name for field in self.parent.fields]

    @property
    def search_fields(self):
        """Returns search_fields for django admin config."""
        return [field.name for field in self.parent.fields if field.is_sk]

    @property
    def templates_root(self):
        """Returns path of templates."""
        return self._path(Path('templates') / self.path_base)

    @property
    def templates_app(self):
        """Returns path of app in templates."""
        return self.path / 'templates' / self.app_name

    @property
    def static_app(self):
        """Returns path of app in static directory."""
        return self.path / 'static' / self.app_name

    @property
    def static_app_css(self):
        """Returns css path of app in static directory."""
        return self.static_app / 'css'

    @property
    def static_app_js(self):
        """Returns javascript path of app in static directory."""
        return self.static_app / 'js'

    @property
    def static_app_img(self):
        """Returns img path of app in static directory."""
        return self.static_app / 'img'

    @property
    def widgets_app(self):
        """Returns widgets path of app in templates directory."""
        return self.templates_app.parent / 'widgets'

    @property
    def widgets_root(self):
        """Returns widgets root in templates directory."""
        return self._path(Path('templates') / 'widgets')

    @property
    def fixtures(self):
        """Returns path of fixtures."""
        return self.path / 'fixtures'

    @property
    def templatetags(self):
        """Returns path of templatetags."""
        return self.path / 'templatetags'

    def update_nspace_djapp(self, nspace):
        """Updates internal namespace."""
        nspace['url'] = self.url
        nspace['url_parent'] = self.url_parent
        nspace['url_index'] = self.url_index
        nspace['url_list'] = self.url_list
        nspace['url_create'] = self.url_create
        nspace['url_detail'] = self.url_detail
        nspace['url_update'] = self.url_update
        nspace['url_delete'] = self.url_delete

        nspace['templates_app'] = str(self.templates_app)
        nspace['templates_root'] = str(self.templates_root)

        nspace['static_app'] = str(self.static_app)
        nspace['static_app_css'] = str(self.static_app_css)
        nspace['static_app_js'] = str(self.static_app_js)
        nspace['static_app_img'] = str(self.static_app_img)

        nspace['widgets_app'] = str(self.widgets_app)
        nspace['widgets_root'] = str(self.widgets_root)

        nspace['fixtures'] = str(self.fixtures)
        nspace['templatetags'] = str(self.templatetags)

        nspace['list_display'] = self.list_display
        nspace['search_fields'] = self.search_fields

    @property
    def to_dict(self):
        """Returns a dict of key attributes."""
        nspace = self._nspace

        # update core attributes
        self.update_nspace_core(nspace)

        # update djapp attributes
        self.update_nspace_djapp(nspace)

        return nspace
