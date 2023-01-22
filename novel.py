# ok

class Novel:
    def __init__(self, title, latest_chapter, link):
        self.link = link
        self.title = title
        self.latest_chapter = latest_chapter

    def __str__(self):
        return f"Title: {self.title}, latest chapter: {self.latest_chapter}, link: {self.link}"

    def __repr__(self):
        return f'Novel(title = {self.title}, latest_chapter = {self.latest_chapter}, link = {self.link})'
