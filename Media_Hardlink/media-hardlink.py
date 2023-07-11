import os
import PTN
import argparse

# Global variables
source_dir_base = "/volume1/Mediax/Downloads/complete"
destination_dir_base = "/volume1/Mediax/"

def setup_argparse() -> dict:
    parser = argparse.ArgumentParser(description='Hardlink media files')
    parser.add_argument('--source', type=str, required=True, help='Source directory of the media')
    return vars(parser.parse_args())

def parse_source(source: str) -> dict:
    links = []
    if os.path.isdir(source):
        for file in os.listdir(source):
            file_path = os.path.join(source, file)
            if os.path.isdir(file_path):
                subdir = parse_source(file_path)
                for item in subdir:
                    links.append(item)
            else:
                filename = os.path.basename(file)
                file_info = parse_file_name(filename)
                if file_info:
                    if 'season' not in file_info:
                        links.append({
                            'source': f"{source}/{file}",
                            'destination': build_destination_dir('movie', file_info['title'])
                        })
                    else:
                        links.append({
                            'source': f"{source}/{file}",
                            'season': file_info['season'],
                            'destination': build_destination_dir('tv', file_info['title'], file_info['season'])
                        })
    else:
        filename = os.path.basename(source)
        file_info = parse_file_name(filename)
        if file_info:
            if 'season' not in file_info:
                links.append({
                    'source': source,
                    'destination': build_destination_dir('movie', file_info['title'])
                })
            else:
                links.append({
                    'source': source,
                    'season': file_info['season'],
                    'destination': build_destination_dir('tv', file_info['title'], file_info['season'])
                })

    return links

def parse_file_name(file_name: str) -> dict or None:
    parsed_file = PTN.parse(file_name)
    return parsed_file if len(parsed_file) > 1 else None

def build_destination_dir(media_type: str, media_name: str, season: int = None) -> str:
    if media_type == 'tv':
        dest_dir = os.path.join(destination_dir_base, "TVShows", media_name)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    else:
        dest_dir = os.path.join(destination_dir_base, "Movies", media_name)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

    return dest_dir

def hardlink_media(items: dict):
    try:
        media_type = 'TV Show' if 'season' in items[0] else 'Movie'
        print(f"Hardlinking {len(items)} items for *{media_type}*")
        for item in items:
            dest_file = None
            if 'season' not in item:
                dest_dir = item['destination']
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                dest_file = os.path.join(dest_dir, os.path.basename(item['source']))
            else:
                dest_dir = os.path.join(item['destination'], f"Season {item['season']}")
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                dest_file = os.path.join(dest_dir, os.path.basename(item['source']))
            os.link(item['source'], dest_file)
    except OSError as e:
        print(f"Error while hardlinking: {e}")

def main():
    # Setup inputs
    args = setup_argparse()
    source = args['source']
    # Parse source
    items = parse_source(source)
    # Run in preview mode
    preview_mode_input = input("Preview mode? (Y/n): ")
    preview_mode = preview_mode_input.lower() == 'y' or preview_mode_input == ''
    if not preview_mode:
        hardlink_media(items)
        print("Done")
    else:
        print(f"Preview mode. {len(items)} items found")
        [print(item) for item in items]

if __name__ == "__main__":
    main()