from tethys_sdk.base import TethysAppBase, url_map_maker


class UtahAlgalBlooms(TethysAppBase):
    """
    Tethys app class for Utah Algal Blooms.
    """

    name = 'Utah Algal Blooms'
    index = 'utah_algal_blooms:home'
    icon = 'utah_algal_blooms/images/FB.jpg'
    package = 'utah_algal_blooms'
    root_url = 'utah-algal-blooms'
    color = '#06148f'
    description = 'An app to track algal blooms in water bodies across the state of Utah'
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
            UrlMap(
                name='new_bloom',
                url='new_bloom',
                controller='utah_algal_blooms.controllers.new_bloom'
            ),
            UrlMap(
                name='map_blooms',
                url='map_blooms',
                controller='utah_algal_blooms.controllers.map_blooms'
            ),
            UrlMap(
                name='list_blooms',
                url='list_blooms',
                controller='utah_algal_blooms.controllers.list_blooms'
            ),
            UrlMap(
                name='info',
                url='info',
                controller='utah_algal_blooms.controllers.info'
            ),
            UrlMap(
                name='help',
                url='help',
                controller='utah_algal_blooms.controllers.help'
            ),
        )

        return url_maps