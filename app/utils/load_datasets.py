"""
This script provides functionalities to import and process data from CSV files into a Django database model,
specifically handling movies, their tags, and external links.

Functions:
    spinner:
        Runs a simple CLI spinner indicating loading or processing status.

    transform_title(title: str):
        Transforms movie titles to a standardized format and extracts the year.
        Handles titles formatted as "Title, The (Year)" and "Title (Year)".

    process_movies(chunk: pd.DataFrame):
        `movies.csv:  [movieId, title,   genres]`
        Processes a chunk of movie data, transforming titles and saving to the database.
        Uses bulk_create for efficient database insertion.

    process_tags(chunk: pd.DataFrame):
        'tags.csv:    [userId,  movieId, tag,    timestamp]'
        Aggregates tags for movies and updates the respective movie entries in the database.

    process_links(chunk: pd.DataFrame):
        'links.csv:   [movieId, imdbId,  tmdbId]'
        Processes movie external link data and updates the movie entries with IMDb and TMDb IDs.

    import_csv(file_path: str, process_function: Callable):
        Asynchronously processes a CSV file in chunks, applying the given processing function.

    run(dataset_path: str):
        Orchestrates the entire data loading and processing workflow.
        Deletes existing Movie entries and sequentially processes movies, tags, and links CSV files.

    load_data(dataset_path: str):
        Entry point to run the data import and processing routine.

Usage:
    To use this script, ensure you have a Django environment set up with the Movie model.
    Call `load_data` with the path to your dataset directory.

    Example:
        load_data("path/to/ml-20m/dataset")

Constants:
    CHUNK_SIZE (int): Defines the size of each chunk to read from CSV files.
"""

import re
import time
import itertools
import threading
import pandas as pd
import asyncio

from asgiref.sync import sync_to_async
from pathlib import Path

from app.models import Movie

CHUNK_SIZE = 500_000


def spinner():
    spinner = itertools.cycle(["-", "/", "|", "\\"])
    while not done:
        print(f"\r{next(spinner)} Loading...", end="", flush=True)
        time.sleep(0.2)


def transform_title(title):
    pattern = r'^(?:"?(.+), The \((\d{4})\)"?|"?([^"]+) \((\d{4})\)"?)$'
    match = re.match(pattern, title)

    if match:
        # Check which pattern was matched
        if match.group(2):
            # "Title, The (Year)" pattern
            return f"The {match.group(1)}", match.group(2)
        else:
            # "Title (Year)" pattern
            return match.group(3), match.group(4)

    return title, None  # Return the original title and None for the year if no match


def process_movies(chunk):
    movie_dicts = chunk.to_dict("records")

    movies = []
    for movie_dict in movie_dicts:
        title, year = transform_title(movie_dict["title"])

        movie = Movie(
            id=movie_dict["movieId"],
            title=title,
            year=year,
            genres=movie_dict["genres"],
        )
        movies.append(movie)

    Movie.objects.bulk_create(movies, ignore_conflicts=True)


def process_tags(chunk):
    aggregated_tags = (
        chunk.groupby("movieId")["tag"]
        .apply(lambda x: ", ".join(set(x.astype(str))))
        .reset_index()
    )

    movies_to_update = []
    for _, row in aggregated_tags.iterrows():
        movie_id, tags = row["movieId"], row["tag"]
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.tags = tags
            movies_to_update.append(movie)
        except Movie.DoesNotExist:
            continue

    Movie.objects.bulk_update(movies_to_update, ["tags"])


def process_links(chunk):
    chunk = chunk.copy()
    chunk["imdbId"] = chunk["imdbId"].fillna(0).astype(int).astype(str).str.zfill(7)
    chunk["tmdbId"] = chunk["tmdbId"].fillna(0).astype(int).astype(str)

    movies_to_update = []
    movie_ids = chunk["movieId"].tolist()
    existing_movies = {
        movie.id: movie for movie in Movie.objects.filter(id__in=movie_ids)
    }

    for _, row in chunk.iterrows():
        movie_id = row["movieId"]
        imdb_id = row["imdbId"]
        tmdb_id = row["tmdbId"]

        if movie_id in existing_movies:
            movie = existing_movies[movie_id]
            movie.imdb_id = imdb_id
            movie.tmdb_id = tmdb_id
            movies_to_update.append(movie)

    Movie.objects.bulk_update(movies_to_update, ["imdb_id", "tmdb_id"])


async def import_csv(file_path, process_function):
    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
        await sync_to_async(process_function)(chunk)


async def run(dataset_path: str):
    global done
    done = False  # type: ignore[name-defined]
    spinner_thread = threading.Thread(target=spinner)

    path = Path(dataset_path)

    await sync_to_async(Movie.objects.all().delete)()

    start_time = time.time()
    try:
        spinner_thread.start()
        await import_csv(path / "movies.csv", process_movies)
        await import_csv(path / "tags.csv", process_tags)
        await import_csv(path / "links.csv", process_links)
    finally:
        done = True  # type: ignore[name-defined]
        spinner_thread.join()

    print(f"\n\nTotal Time: {round((time.time() - start_time), 1)} second")


def load_data(dataset_path: str):
    asyncio.run(run(dataset_path))
