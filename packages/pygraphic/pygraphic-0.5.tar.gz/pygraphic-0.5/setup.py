# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygraphic']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.5.1,<0.6.0', 'pydantic>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'pygraphic',
    'version': '0.5',
    'description': 'Client-side GraphQL query generator based on Pydantic',
    'long_description': '# pygraphic\n<p>\n<a href="https://pypi.org/project/pygraphic" target="_blank">\n    <img src="https://img.shields.io/pypi/status/pygraphic" alt="Status">\n</a>\n<a href="https://pypi.org/project/pygraphic" target="_blank">\n    <img src="https://img.shields.io/pypi/v/pygraphic" alt="Version">\n</a>\n<a href="https://github.com/lonelyteapot/pygraphic/actions/workflows/test.yml?query=branch%3Amain" target="_blank">\n    <img src="https://img.shields.io/github/workflow/status/lonelyteapot/pygraphic/Unit%20tests/main?label=tests" alt="Tests">\n</a>\n<a href="https://codecov.io/gh/lonelyteapot/pygraphic" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/lonelyteapot/pygraphic" alt="Coverage">\n</a>\n</p>\n\nClient-side GraphQL query generator based on [pydantic].\n\n## Why?\n\nWorking with GraphQL in Python seems simple... If you\'re fine with dictionaries, lack of\nautocompletion and unexpected errors.\n\nSome tools allow you to generate Python code from GraphQL schemas. One of them, [turms],\neven generates pydantic models from GQL documents. This approach can be problematic:\nqueries are written in GraphQL, not Python, so the codebase you\'re actually working with\nis out of your control; and the main advantage of pydantic — data validation — is\nmissing!\n\n## Workflow\n\nPygraphic is the opposite of [turms]:\n\n1. For each individual query, you define pydantic models that you want to request,\n   optionally with validators and other configuration;\n\n2. Pygraphic converts those definitions to raw GraphQL documents *(basically strings)*;\n\n3. Using a GraphQL or an HTTP client, you make requests with those documents and get\n   back JSON responses;\n\n4. Pydantic converts those responses to instances of the defined models and validates\n   them;\n\n5. You use the validated data, while enjoying autocompletion and type safety!\n\n## Roadmap\n\nPygraphic is in development stage. Some major features are missing or might work\nincorrectly. The API may change at any time.\n\nSee [ROADMAP.md][Roadmap] for the list of implemented/missing features.\n\n## Examples\n\nExamples are kept in the\n[/examples](https://github.com/lonelyteapot/pygraphic/tree/main/examples) folder.  \nQueries that they\'re expected to produce are stored in the\n[/golden_files](https://github.com/lonelyteapot/pygraphic/tree/main/folden_files)\nfolder.\n\nMost examples are based on [GitHub\'s GraphQL API](https://docs.github.com/en/graphql).\nIf you want to run them, you need to \n[generate a personal access token](https://github.com/settings/tokens) and assign it to\nthe environment variable called `GITHUB_TOKEN` (with VSCode, the best way to do this is\nto create a [`.env` file](https://www.dotenv.org/env) in the project\'s root directory).\n\nHere\'s the gist:\n\n### main.py\n\n``` python\nimport os\nimport requests\nfrom pygraphic import GQLQuery, GQLType\n\n# Define data models\nclass License(GQLType):\n    id: str\n    name: str\n    description: str\n\n# Define query model\nclass GetAllLicenses(GQLQuery):\n    licenses: list[License]\n\n# Generate the GraphQL query string\nquery_str = GetAllLicenses.get_query_string()\n\n# Make the request\nTOKEN = os.environ["GITHUB_TOKEN"]\nresponse = requests.post(\n    url="https://api.github.com/graphql",\n    json={\n        "query": query_str,\n    },\n    headers={\n        "Authorization": f"bearer {TOKEN}",\n    },\n)\n\n# Parse the response\nresponse_data = response.json().get(\'data\')\nif response_data is None:\n    print(\'Query failed\')\nresult = GetAllLicenses.parse_obj(response_data)\n\n# Print the results\nfor license in result.licenses:\n    print(license.name)\n```\n\n### Generated query string\n\n``` gql\nquery GetAllLicenses {\n  licenses {\n    id\n    name\n    description\n  }\n}\n```\n\n## Contribution\n\nThis project is developed on [GitHub].\n\nIf you have any general questions or need help — you\'re welcome in the [Discussions]\nsection.\n\nIf you encounter any bugs or missing features — file new [Issues], but make sure to\ncheck the existing ones first.\n\nIf you want to solve an issue, go ahead and create a [Pull Request][Pulls]! It will be\nreviewed and hopefully merged. Help is always appreciated.\n\n## License\n\nCopyright &copy; 2022, Dmitry Semenov. Released under the [MIT license][License].\n\n\n[GitHub]: https://github.com/lonelyteapot/pygraphic\n[Discussions]: https://github.com/lonelyteapot/pygraphic/discussions\n[Issues]: https://github.com/lonelyteapot/pygraphic/issues\n[Pulls]: https://github.com/lonelyteapot/pygraphic/pulls\n[License]: https://github.com/lonelyteapot/pygraphic/blob/main/LICENSE\n[Roadmap]: https://github.com/lonelyteapot/pygraphic/blob/main/ROADMAP.md\n\n[pydantic]: https://pypi.org/project/pydantic/\n[turms]: https://pypi.org/project/turms/\n',
    'author': 'Dmitry Semenov',
    'author_email': 'lonelyteapot@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lonelyteapot/pygraphic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
