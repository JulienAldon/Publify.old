| rule  |      route          |   description                           |
--------|---------------------|-----------------------------------------| 
|GET    | /playlist           | # Return a playlist list                |
|POST   | /playlist           | # Create a new playlist synchronization |
|GET    | /playlist/<id>      | # Return a playlist's information       |
|PUT    | /playlist/<id>      | # Update a playlist                     |
|DELETE | /playlist/<id>      | # Remove a synchronization link         |
|GET    | /playlist/<id>/sync | # Get synchronization status for playlist|
|PUT    | /playlist/<id>/sync | # Request synchronization of a playlist |

Playlists
    - get /playlist return playlist list (name & id)
    - post /playlist create a playlist link

PlaylistLink
    - get /playlist/<id> give playlist link info
    - put /playlist/<id> update a playlist link
    - delete /playlist/<id> remove a playlist link

Synchronizer
    - get /playlist/<id>/sync
    - put /playlist/<id>/sync

Special Methods
 * PUT    /playlist/all/sync  # Synchronize all playlists for this account
 * GET    /playlist/all/sync  # Get synchronization state for all playlists