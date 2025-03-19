from flask import Flask, jsonify, render_template, url_for, redirect
from flask_frozen import Freezer
import os
import frontmatter
import markdown
import json
import shutil
from collections import defaultdict

app = Flask(__name__)
freezer = Freezer(app)

def load_content(directory='content', parent_path=''):
    """
    Recursively load content from a directory structure.
    Returns a dictionary of paths to content files and a directory structure.
    """
    content_dict = {}
    directory_structure = defaultdict(dict)

    if not os.path.exists(directory):
        return content_dict, directory_structure

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        relative_path = os.path.join(parent_path, item)

        if os.path.isdir(item_path):
            # Handle directories
            dir_name = item
            # Recursively process subdirectory
            sub_content, sub_structure = load_content(item_path, relative_path)
            content_dict.update(sub_content)

            # Add directory to structure
            directory_structure[dir_name] = sub_structure

            # Check for index.md in directory
            index_path = os.path.join(item_path, 'index.md')
            if os.path.exists(index_path):
                url_path = relative_path.replace('\\', '/')
                content_dict[url_path] = load_markdown_file(index_path, url_path)

        elif item.endswith('.md'):
            # Handle markdown files
            url_path = relative_path.replace('\\', '/').replace('.md', '')
            content_dict[url_path] = load_markdown_file(item_path, url_path)

    return content_dict, directory_structure

def load_markdown_file(filepath, url_path):
    """
    Load a markdown file and return its content and metadata.
    """
    md = markdown.Markdown(extensions=['codehilite', 'fenced_code', 'toc'])

    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        metadata = post.metadata
        content_html = md.convert(post.content)

        # Extract TOC if available
        toc = md.toc if hasattr(md, 'toc') else ""

        # Set default title if not provided
        if 'title' not in metadata:
            metadata['title'] = os.path.basename(filepath).replace('.md', '').replace('_', ' ').title()
            if metadata['title'].lower() == 'index':
                # For index.md files, use the parent directory name as title
                parent_dir = os.path.basename(os.path.dirname(filepath))
                metadata['title'] = parent_dir.replace('_', ' ').title() if parent_dir else 'Home'

        return {
            'metadata': metadata,
            'content_html': content_html,
            'toc': toc,
            'url_path': url_path
        }

# Load content
CONTENT, DIRECTORY_STRUCTURE = load_content()

def get_breadcrumbs(path):
    """
    Generate breadcrumbs for a given path.
    """
    breadcrumbs = [{'name': 'Home', 'url': '/'}]

    if path == '':
        return breadcrumbs

    parts = path.split('/')
    current_path = ''

    for part in parts:
        if part:
            current_path += f'/{part}'
            part_name = part.replace('-', ' ').replace('_', ' ').title()
            breadcrumbs.append({'name': part_name, 'url': current_path})

    return breadcrumbs

def get_siblings(path):
    """
    Get sibling pages for a given path.
    """
    if path == '':
        return []

    parts = path.split('/')
    parent_path = '/'.join(parts[:-1])

    # Get all content that shares the same parent path
    siblings = []
    for content_path, content in CONTENT.items():
        if content_path != path and content_path.startswith(parent_path):
            parts = content_path.split('/')
            if len(parts) == len(path.split('/')) and parts[:-1] == path.split('/')[:-1]:
                siblings.append({
                    'title': content['metadata'].get('title', parts[-1].replace('-', ' ').replace('_', ' ').title()),
                    'url': f'/{content_path}.html'  # Add .html extension for Frozen-Flask
                })

    return siblings

def get_chapter_listing(path):
    """
    Get a listing of chapters for a given path.
    """
    current_dir = path.split('/') if path else []

    # Navigate to the correct point in the directory structure
    current_struct = DIRECTORY_STRUCTURE
    for part in current_dir:
        if part in current_struct:
            current_struct = current_struct[part]

    # Extract chapters (directories) from the current structure
    chapters = []
    for dir_name, _ in current_struct.items():
        # Check if this directory has an index.md
        dir_path = '/'.join(current_dir + [dir_name]) if current_dir else dir_name
        if dir_path in CONTENT:
            chapters.append({
                'title': CONTENT[dir_path]['metadata'].get('title', dir_name.replace('_', ' ').title()),
                'url': f'/{dir_path}.html'  # Add .html extension for Frozen-Flask
            })

    return chapters

# Root route redirects to index.html
@app.route('/')
def root():
    return redirect('/index.html')

# Route for any content path
@app.route('/<path:path>')
def content_page(path):
    # Strip .html extension if present (for compatibility with frozen flask)
    if path.endswith('.html'):
        path = path[:-5]

    # Normalize path
    path = path.rstrip('/')

    # Try to find the content
    content = CONTENT.get(path)
    if not content:
        return "Page not found", 404

    # Generate breadcrumbs
    breadcrumbs = get_breadcrumbs(path)

    # Get siblings for navigation
    siblings = get_siblings(path)

    # Get chapter listing if this is an index
    chapters = get_chapter_listing(path)

    # Get children (subpages)
    children = []
    for content_path, content_data in CONTENT.items():
        if content_path != path and content_path.startswith(path + '/'):
            parts = content_path.split('/')
            if len(parts) == len(path.split('/')) + 1:
                children.append({
                    'title': content_data['metadata'].get('title', parts[-1].replace('-', ' ').replace('_', ' ').title()),
                    'url': f'/{content_path}.html'  # Add .html extension for Frozen-Flask
                })

    return render_template(
        'content.html',
        content=content,
        breadcrumbs=breadcrumbs,
        siblings=siblings,
        chapters=chapters,
        children=children,
        path=path
    )

# Modify the freezer generator to add .html extension
@freezer.register_generator
def content_page():
    for path in CONTENT:
        yield {'path': f"{path}.html"}

# Add generator for root path
@freezer.register_generator
def root():
    yield {}

if __name__ == '__main__':
    app.run(debug=True)
    # freezer.freeze()  # Generate static files