
Get a single user
~~~~~~~~~~~~~~~~~

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/details/55

.. http:method:: GET /api/0.1/user/details/{id}

   :arg id: user id.

.. http:response:: Retrieve user details by id.

   .. sourcecode:: js

		{
		  "date_joined": "2013-12-10T22:20:50.060012",
		  "description": "Developer",
		  "email": "alexander.salas@gmail.com",
		  "first_name": "Alexander Javier",
		  "id": 55,
		  "last_login": "2014-02-26T19:58:04.112944",
		  "last_name": "Salas Bastidas",
		  "location": null,
		  "resource_uri": "/api/0.1/user/details/55",
		  "telefono": null,
		  "user_profile": "/api/0.1/user/profile/55",
		  "username": "alexandersalas"
		}

Get the authenticated user
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/details

.. http:method:: GET /api/0.1/user/details

.. http:response:: Retrieve user details.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 1
		  },
		  "objects": [
			{
			  "date_joined": "2013-12-10T22:20:50.060012",
			  "description": "Developer",
			  "email": "alexander.salas@gmail.com",
			  "first_name": "Alexander Javier",
			  "id": 55,
			  "last_login": "2014-02-26T19:58:04.112944",
			  "last_name": "Salas Bastidas",
			  "location": null,
			  "resource_uri": "/api/0.1/user/details/55",
			  "telefono": null,
			  "user_profile": "/api/0.1/user/profile/55",
			  "username": "alexandersalas"
			}
		  ]
		}

Get all users
~~~~~~~~~~~~~
This provides all user profile.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/profile

.. http:method:: GET /api/0.1/user/details

.. http:response:: Retrieve the first 20 users profile on tribus.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": "/api/0.1/user/profile?limit=20&offset=20",
			"offset": 0,
			"previous": null,
			"total_count": 210
		  },
		  "objects": [
			{
			  "followers": [
				
			  ],
			  "follows": [
				
			  ],
			  "id": 37,
			  "resource_uri": "/api/0.1/user/profile/37",
			  "user": "/api/0.1/user/details/37"
			}
		  ]
		}
		
List followers of a user
~~~~~~~~~~~~~~~~~~~~~~~~
List a user’s followers.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/followers/55

.. http:method:: GET /api/0.1/user/followers/{id}

   :arg id: user id.

.. http:response:: Retrieve the first 20 followers from the id.

   .. sourcecode:: js

		Unimplemented

List the authenticated user’s followers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/followers

.. http:method:: GET /api/0.1/user/followers

.. http:response:: Retrieve the first 20 followers.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 8
		  },
		  "objects": [
			{
			  "date_joined": "2013-12-10T23:39:48.460212",
			  "description": "Este es mi perfil en Tribus!",
			  "email": "el.wuilmer@gmail.com",
			  "first_name": "Wuilmer",
			  "id": 59,
			  "last_login": "2014-02-26T20:29:58.903555",
			  "last_name": "Bolivar",
			  "location": null,
			  "resource_uri": "/api/0.1/user/followers/59",
			  "telefono": null,
			  "username": "ElWuilMeR"
			}
		  ]
		}
		
List of follows of a user
~~~~~~~~~~~~~~~~~~~~~~~~
List a user’s follows:

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/follows

.. http:method:: GET /api/0.1/user/follows/{id}

   :arg id: user id.

.. http:response:: Retrieve the first 20 followed users from the id.

   .. sourcecode:: js
   
		Unimplemented
		
List the authenticated user’s follows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/follows

.. http:method:: GET /api/0.1/user/follows

.. http:response:: Retrieve the first 20 follows.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 6
		  },
		  "objects": [
			{
			  "date_joined": "2013-12-10T23:39:48.460212",
			  "description": "Este es mi perfil en Tribus!",
			  "email": "el.wuilmer@gmail.com",
			  "first_name": "Wuilmer",
			  "id": 59,
			  "last_login": "2014-02-26T20:29:58.903555",
			  "last_name": "Bolivar",
			  "location": null,
			  "resource_uri": "/api/0.1/user/follows/59",
			  "telefono": null,
			  "username": "ElWuilMeR"
			}
		  ]
		}
		
Get all tribs
~~~~~~~~~~~~~
This provides all post on tribus ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/tribs

.. http:method:: GET /api/0.1/user/tribs

.. http:response:: Retrieve the first 20 posts on tribus.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": "/api/0.1/user/tribs?limit=20&offset=20",
			"offset": 0,
			"previous": null,
			"total_count": 79
		  },
		  "objects": [
			{
			  "author_email": "luis@huntingbears.com.ve",
			  "author_first_name": "Luis Alejandro",
			  "author_id": 8,
			  "author_last_name": "MartÃ­nez Faneyth",
			  "author_username": "HuntingBears",
			  "id": "52a3f386ff600f7079173e7d",
			  "resource_uri": "/api/0.1/user/tribs/52a3f386ff600f7079173e7d",
			  "trib_content": "Este es mi primer mensaje en Tribus.",
			  "trib_pub_date": "2013-12-07T20:20:40.541Z"
			}
		  ]
		}
		
Get all tribs from author
~~~~~~~~~~~~~~~~~~~~~~~~~~
This provides all post from the author ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/tribs/55

.. http:method:: GET /api/0.1/user/tribs/{author_id}

   :arg author_id: user id.

.. http:response:: Retrieve the first 20 tribs from the id author.

   .. sourcecode:: js
   
		Unimplemented

		
Get all comments of tribs
~~~~~~~~~~~~~~~~~~~~~~~~~
This provides all comments from all tribs ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/tribs/comments

.. http:method:: GET /api/0.1/tribs/comments

.. http:response:: Retrieve the first 20 comments of all tribs.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": "/api/0.1/tribs/comments?limit=20&offset=20",
			"offset": 0,
			"previous": null,
			"total_count": 58
		  },
		  "objects": [
			{
			  "author_email": "luis@huntingbears.com.ve",
			  "author_first_name": "Luis Alejandro",
			  "author_id": 8,
			  "author_last_name": "MartÃ­nez Faneyth",
			  "author_username": "HuntingBears",
			  "comment_content": "Este es mi primer comentario en Tribus.",
			  "comment_pub_date": "2013-12-07T20:20:55.370Z",
			  "id": "52a3f395ff600f7079173e7e",
			  "resource_uri": "/api/0.1/tribs/comments/52a3f395ff600f7079173e7e",
			  "trib_id": "52a3f386ff600f7079173e7d"
			}
		  ]
		}

		
Get all comments of trib
~~~~~~~~~~~~~~~~~~~~~~~~
This provides all comments from the trib id ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/tribs/comments/52a3f386ff600f7079173e7d

.. http:method:: GET /api/0.1/tribs/comments/{trib_id}

   :arg trib_id: trib id.

.. http:response:: Retrieve the first 20 comments of the trib.

   .. sourcecode:: js

		Unimplemented
		
Search User or Package Resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:method:: GET /api/0.1/search?q={search_term}

   :arg search_term: Perform search with this term.
   
::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/search?q=luisalejandro
    

.. http:response:: Retrieve a list of Users objects that contain the search term.

   .. sourcecode:: js
   
		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 1
		  },
		  "objects": [
			{
			  "packages": [
				
			  ],
			  "users": [
				{
				  "fullname": "Luis Alejandro MartÃ­nez Faneyth",
				  "username": "luisalejandro"
				}
			  ]
			}
		  ]
		}
		
::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/search?q=0ad
    

.. http:response:: Retrieve a list of Package objects that contain the search term.

   .. sourcecode:: js
   
		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 1
		  },
		  "objects": [
			{
			  "packages": [
				{
				  "name": "0ad-data"
				},
				{
				  "name": "0ad"
				},
				{
				  "name": "0ad-dbg"
				}
			  ],
			  "users": [
				
			  ]
			}
		  ]
		}
