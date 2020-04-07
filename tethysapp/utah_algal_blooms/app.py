from tethys_sdk.base import TethysAppBase, url_map_maker


class UtahAlgalBlooms(TethysAppBase):
    """
    Tethys app class for Utah Algal Blooms.
    """

    name = 'Utah Algal Blooms'
    index = 'utah_algal_blooms:home'
    icon = 'utah_algal_blooms/images/icon.gif'
    package = 'utah_algal_blooms'
    root_url = 'utah-algal-blooms'
    color = '#f39c12'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='utah-algal-blooms',
                controller='utah_algal_blooms.controllers.home'
            ),
        )

        return url_maps