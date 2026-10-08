"""Catch omitted translations, broken project routes and lost migration links."""
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def frontmatter(path):
    return yaml.safe_load(path.read_text(encoding='utf-8').split('---', 2)[1])

class ContentTests(unittest.TestCase):
    def test_all_original_projects_have_two_complete_translations(self):
        originals = {str(frontmatter(p)['modal-id']) for p in (ROOT / '_posts').glob('*.markdown')}
        shared = yaml.safe_load((ROOT / '_data/projects.yml').read_text(encoding='utf-8'))
        self.assertEqual({str(p['legacy_id']) for p in shared.values() if 'legacy_id' in p}, originals)
        self.assertEqual(len(shared), 19)
        routes = set()
        for project_id, metadata in shared.items():
            for lang, prefix in [('en', ''), ('pl', '/pl')]:
                path = ROOT / '_projects' / lang / (project_id + '.md')
                data = frontmatter(path)
                self.assertEqual(data['project_id'], project_id)
                self.assertEqual(data['lang'], lang)
                self.assertEqual(data['permalink'], f'{prefix}/projects/{project_id}/')
                self.assertNotIn(data['permalink'], routes)
                routes.add(data['permalink'])
                body = path.read_text(encoding='utf-8').split('---', 2)[2]
                self.assertEqual(body.count('\n## '), 4)
                self.assertGreater(len(data['description']), 30)
            self.assertTrue((ROOT / metadata['image'].lstrip('/')).is_file())
            for figure in metadata.get('gallery', []):
                self.assertTrue((ROOT / figure['src'].lstrip('/')).is_file())

    def test_orifice_website_is_separate_bilingual_software_case_study(self):
        shared = yaml.safe_load((ROOT / '_data/projects.yml').read_text(encoding='utf-8'))
        self.assertIn('orifice-website', shared)
        meta = shared['orifice-website']
        self.assertEqual(meta['category'], 'software')
        self.assertNotIn('legacy_id', meta)
        self.assertEqual(sum(p['category'] == 'software' for p in shared.values()), 6)
        self.assertIn('https://orifice-software.com/', meta['references'])
        images = yaml.safe_load((ROOT / '_data/images.yml').read_text(encoding='utf-8'))
        for src in [meta['image']] + [f['src'] for f in meta['gallery']]:
            self.assertIn(src, images)
            self.assertGreater(images[src]['width'], 1000)
            self.assertTrue((ROOT / images[src]['src'].lstrip('/')).is_file())
        for lang, prefix in [('en', ''), ('pl', '/pl')]:
            path = ROOT / '_projects' / lang / 'orifice-website.md'
            data = frontmatter(path)
            self.assertEqual(data['order'], 18)
            self.assertEqual(data['featured'], 0)
            self.assertIn(f'{prefix}/projects/orifice-calculation-software/', path.read_text(encoding='utf-8'))

    def test_translated_interface_keys_match(self):
        translations = yaml.safe_load((ROOT / '_data/i18n.yml').read_text(encoding='utf-8'))
        self.assertEqual(set(translations['en']), set(translations['pl']))
        self.assertEqual(set(translations['en']['categories']), set(translations['pl']['categories']))

    def test_case_studies_retain_reported_validation_results(self):
        for lang, decimals in [('en', ('1.82%', '−1.54%')), ('pl', ('1,82%', '−1,54%'))]:
            orifice = (ROOT / '_projects' / lang / 'four-hole-orifice.md').read_text(encoding='utf-8')
            for value in decimals:
                self.assertIn(value, orifice)
            energy = (ROOT / '_projects' / lang / 'energy-techno-economics.md').read_text(encoding='utf-8')
            self.assertIn('98%', energy)

if __name__ == '__main__':
    unittest.main()
