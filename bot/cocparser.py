import json
import discord


class CoCData():
    def construct(self, **kwargs):
        self.__dict__.update(kwargs)


def load_coc_data_from_file(data: CoCData, filepath: str):
    try:
        data.construct(**json.loads(open(filepath).read())['coc'])
    except IOError:
        print(f'Failed to open CoC file!: {filepath}')
    except json.JSONDecodeError:
        print('Invalid JSON provided!')
    except KeyError:
        print('No `coc` key provided in file, cannot parse this CoC file')


def prepare_coc_header(header: dict):
    header_subposts = []
    for s in header['sections']:
        if s['type'] == 'paragraph':
            header_subposts.append(discord.Embed(
                title=s['header'],
                description=s['content']
            ))
        elif s['type'] == 'list':
            header_subposts.append(discord.Embed(
                title=s['header'],
                description='\n'.join([f'{x}' for x in s['content']])
            ))
        elif s['type'] == 'numbered_list':
            header_subposts.append(discord.Embed(
                title=s['header'],
                description='\n'.join([f'{idx+1}. {x}' for idx, x in enumerate(s['content'])])
            ))
        else:
            print('Unsupported type provided!')
    return {
        'title': header['title'],
        'headerposts': header_subposts
    }


def prepare_coc_sections(sections: list):
    coc_sections = []

    for section_idx, section in enumerate(sections):
        coc_section_header = discord.Embed(
            title=f'{section_idx+1}.0.0 {section["title"].upper()}'
        )

        thread_posts = []
        for post_idx, post in enumerate(section['items']):
            thread_posts.append(discord.Embed(
                title=f'{section_idx+1}.{post_idx+1}.0 {post["title"]}',
                description=post['content']
            ))

        coc_sections.append({
            'section_header': coc_section_header,
            'section_thread_posts': thread_posts
        })
    return coc_sections


def prepare_coc_post(data: CoCData):
    header_posts = prepare_coc_header(data.header)
    section_posts = prepare_coc_sections(data.sections)

    return {
        'preamble': header_posts,
        'sections': section_posts
    }
