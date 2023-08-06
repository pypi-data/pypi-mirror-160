import yaml
import os


class gitlab_ci:
    def __init__(self, theme, docs_dir):
        self.theme = theme
        self.docs_dir = docs_dir
        self.file_exists = os.path.exists(os.getcwd() + "/.gitlab-ci.yml")
        if self.file_exists:
            with open(".gitlab-ci.yml", "r") as f:
                self.file = yaml.safe_load(f)
        else:
            self.file = {}

        return

    def _createStage(self, name):
        name = name + 'docs'
        if name in self.file['stages']:
            name = self._createStage(name)

        return name

    def addPages(self):
        if self.file_exists and self.file is not None:
            if 'pages' in self.file.keys():
                exit("That's wierd...\
                        looks like you're already deploying docs")
            else:
                self.name = self._createStage("")
                self.file['stages'].append(self.name)
        else:
            self.file = {'stages': ['docs']}
            self.name = 'docs'

        self.file['pages'] = {'stage': f'{self.name}',
                              'image': 'python:latest',
                              'before_script': [
                                'pip install --upgrade pip',
                                'pip install Sphinx',
                                f'pip install {self.theme}'
                                  ],
                              'script':
                              f'sphinx-build -b html {self.docs_dir} public',
                              'artifacts': {'paths': ['public']}}

        return

    def save(self):
        with open(".gitlab-ci.yml", "w") as f:
            yaml.dump(self.file, f, sort_keys=False)

        return
