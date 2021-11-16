from tornado.web import url

import views

routes = [
    url('/', views.HomePageHandler, name='home'),
    url(r'/threads/?', views.ThreadsHandler, name='threads'),
    url(r'/threads/(\w+)/?', views.ThreadsBelongsToAChannel, name="tbelongstoc"),        # noqa E501
    url(r'/threads/([^/]+)/([0-9]+)/?', views.SingleThreadHandler, name='show-thread'),  # noqa E501
    url(r'/threads/([^/]+)/([0-9]+)/replies/?', views.ReplyHandler, name='reply'),       # noqa E501
    url(r'/auth/login/?', views.AuthHandler, name='login'),
    url(r'/auth/logout/?', views.Logout, name='logout'),
]
