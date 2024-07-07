from xlschema.plugins.cmdline import PluginApplication


class Application(PluginApplication):
    "Mock application."

    def cmdline(self, args):
        """Main method and commandline entrypoint."""
        self.set_general_options()
        self._setup_plugins_cmdline()
        options = self.parser.parse_args(args)
        self._setup_plugins(options)
        self._execute_plugins(options)

def test_plugin_import():
    try:
        from xlschema.plugins import echo
    except ImportError as exc:
        assert False, exc

def test_plugin_app():
    app = Application()
    app.cmdline(['echo', 'world'])
    assert app.plugins
