#!/usr/bin/env python3
from pathlib import Path
import glob

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
	<head>
		<title>Distrobox Manifests</title>
		
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	</head>
	
	<body>
		<p>The following manifests are available:</p>
		
		<ul>
			{}
		</ul>
	</body>
</html>
'''

# Retrieve the list of manifests in the directory containing this script
manifests_dir = Path(__file__).parent
manifests = sorted(glob.glob(str(manifests_dir / '*.ini')))
filenames = [Path(manifest).name for manifest in manifests]

# Generate our index HTML file
links = [f'<li><a href="./{ filename }">{ filename }</a></li>' for filename in filenames]
index = HTML_TEMPLATE.format('\n\t\t\t'.join(links))
outfile = manifests_dir / 'index.html'
outfile.write_text(index, 'utf-8')
