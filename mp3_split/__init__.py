"""
Split a long MP3 file into smaller files using a track listing in YAML.
"""

from pathlib import Path
import os
import datetime
import logging
import yaml
import ffmpeg
import click


def timecode_to_secs(timecode):
    """
    Convert a time-ish string into seconds regardless of whether it has hours.
    """

    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(timecode.split(':'))))


def write_outputs(input_file, config_data, artist, album, output_path):
    """
    Use the configured timestamps and metadata to write outputs.
    """

    for track in range(len(config_data["tracks"])-1):
        track_number = str(track+1).zfill(2)
        output_file = f'{output_path}/{track_number} {track_name}.mp3'
        track_name = config_data["tracks"][track]["name"]
        tags = {
            'metadata:g:0': f"artist={artist}",
            'metadata:g:1': f"album={album}",
            'metadata:g:2': f"track_num={track_number}",
            'metadata:g:3': f"title={track_name}",
        }
        start_time = config_data["tracks"][track]["offset"]
        end_time = config_data["tracks"][track+1]["offset"]
        track_length = str(timecode_to_secs(end_time) -
                           timecode_to_secs(start_time))
        _out, err = (
            ffmpeg
            .input(input_file)
            .output(output_file, acodec='copy', **tags, t=track_length, ss=start_time)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        logging.debug(err.decode("utf-8"))


@click.command(no_args_is_help=True)
@click.argument('input_file', type=click.Path("r"), required=True)
@click.argument('config_file', type=click.File("r"), required=True)
def main(input_file, config_file):
    """
    Split INPUT_FILE up into tracks as specified by CONFIG_FILE.
    """

    logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

    try:
        config_data = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        raise exc

    # This is inexact with VBR MP3s, but it is close enough
    duration = str(datetime.timedelta(seconds=int(float(
        ffmpeg.probe(input_file)["streams"][0]['duration'])))
    )
    logging.debug("Audio ends at %s", duration)
    config_data['tracks'].append({'name': 'end', 'offset': duration})

    output_path = Path(f'{config_data["artist"]}/{config_data["album"]}')
    output_path.mkdir(parents=True, exist_ok=True)

    write_outputs(
        input_file, config_data, config_data["artist"], config_data["album"], output_path
    )
