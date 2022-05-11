from tornado.web import url

import views

routes = [
    url("/", views.HomePageHandler, name="home"),
    url(r"/threads/?", views.ThreadsHandler, name="threads"),
    url(r"/threads/create/?", views.CreateAThread, name="createathread"),
    url(
        r"/threads/([^/]+)/([0-9]+)/?", views.ThreadsManager, name="show-thread"
    ),  # noqa E501
    url(
        r"/threads/([^/]+)/([0-9]+)/replies/?", views.AddAReply, name="reply"
    ),  # noqa E501
    url(r"/rp/?", views.RepliesPagination, name="rp"),
    url(
        r"/replies/([0-9]+)/favorites/?",
        views.RepliesFavorites,
        name="replies_favorites",
    ),  # noqa E501
    url(r"/auth/login/?", views.AuthHandler, name="login"),
    url(r"/auth/logout/?", views.Logout, name="logout"),
    url(r"/profiles/(\w+)/?", views.profilesHandler, name="profiles"),
]
