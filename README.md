# Movie Collection Flask Web App

This Flask web application allows users to manage their favorite movie collection. Movie details are fetched from The Movie Database (TMDB) API, and users can add, edit, and delete movies, along with providing ratings and reviews.

-------------
## Functions
-------------

### `home()`
- Renders the home page displaying the user's movie collection.
- Retrieves all movies from the database and passes them to the template.

### `edit_movie()`
- Renders the edit movie page.
- Retrieves the selected movie using the movie ID from the request arguments.
- Handles the submission of the edit form, updating the movie's rating and review in the database.

### `add_movie()`
- Renders the add movie page.
- Handles the submission of the add form, fetching movie details from TMDB API and displaying search results.
- Allows users to select a movie from search results to add to their collection.

### `delete_movie()`
- Deletes a movie from the collection based on the provided movie ID.
- Displays success or error messages accordingly.

### `find_movie()`
- Fetches additional details for a movie from TMDB API based on the provided TMDB movie ID.
- Adds the movie to the user's collection and redirects to the edit page.

-------------
## Variables
-------------

### `app`
- Flask application instance.

### `db`
- SQLAlchemy database instance.

### `TMDB_IMAGE_URL`
- Base URL for fetching movie images from TMDB.

### `TMDB_ACCESS_TOKEN`
- TMDB API access token.

### `TMDB_API_KEY`
- TMDB API key.

### `headers`
- Headers used in TMDB API requests.

### `Movie`
- SQLAlchemy model representing a movie in the database.

### `EditForm`
- WTForms form for editing movie details (rating and review).

### `AddForm`
- WTForms form for adding a new movie.

---------
## Usage
---------

1. Install the required packages: `pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Bootstrap python-dotenv requests`.

2. Set up your TMDB API access by obtaining an API key.

3. Create a `.env` file in the project root with the following content:

4. Run the application: `python your_app_file.py`.

5. Open your browser and navigate to `http://localhost:5000` to use the application.

