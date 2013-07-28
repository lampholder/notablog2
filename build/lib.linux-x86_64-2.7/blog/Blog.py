# This python file uses the followin encoding: utf-8

import glob, os, re, codecs, hashlib
from datetime import datetime
import cherrypy
import pystache
import PyRSS2Gen

ENTRIES_PATH = 'entries/'

class _EntryFileWrangler:

  @staticmethod
  def get_details(entry_path):
    global ENTRIES_PATH
    filename = entry_path.replace(ENTRIES_PATH, '', 1).replace('./', '', 1)
    match = re.match('^(.*?)\.([0-9]{10,11})\.entry$', filename)
    if match is not None:
      published_date = int(match.group(2))
      title = match.group(1) + '.entry'
    else:
      published_date = _EntryFileWrangler.get_os_date(entry_path)
      title = filename
    return {'filename': filename,
            'published_date': published_date,
            'title': title,
            'tag': _EntryFileWrangler.get_hashtag(filename)}

  @staticmethod
  def get_os_date(entry_path):
    return int(os.path.getmtime(entry_path))

  @staticmethod
  def get_hashtag(filename):
    return hashlib.md5(filename).digest().encode("base64")[0:8]

class _Api:

  def __init__(self):
    self._entries_path = './entries/'

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def entries(self):
    return sorted([_EntryFileWrangler.get_details(filename)
                  for filename in glob.glob(os.path.join(self._entries_path, '*.entry'))], key=lambda x: x['published_date'], reverse=True)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def entry(self, filename):
    safe_filename = filename.replace('/', '').lstrip('.')
    entry_path = 'entries/%s' % safe_filename
    details = _EntryFileWrangler.get_details(entry_path)
    details['content'] = codecs.open(entry_path, 'r', 'utf-8').read()

    return details

class Blog:

  def __init__(self):
    PAGE = 'templates/index.template'
    ENTRY = 'templates/entry.template'

    self._page_template = file(PAGE).read()
    self._entry_template = file(ENTRY).read()
    self._entries_path = './entries/'

    self.api = _Api()
    self._filtr = Filtr()

  def _format_entry(self, filename):
    full_entry = self.api.entry(filename)
    full_entry['twitter_id'] = 'lampholder'
    full_entry['content'] = self._filtr.unswear(full_entry['content'])
    full_entry['published_date'] = datetime.fromtimestamp(float(full_entry['published_date'])).strftime("%a, %d %b %Y %H:%M:%S UTC")
    return pystache.render(self._entry_template, full_entry)

  @cherrypy.expose
  def entries(self):
    entries = '<hr>\n'.join([self._format_entry(entry['filename']) for entry in self.api.entries()])
    return pystache.render(self._page_template, {'content': entries})

  @cherrypy.expose
  def entry(self, filename):
    entry = self._format_entry(filename)
    return pystache.render(self._page_template, {'content': entry})

  @cherrypy.expose
  def rss(self):
    cherrypy.response.headers['Content-Type']= 'text/xml'
    entries = self.api.entries()
    rss = PyRSS2Gen.RSS2(
      title = "Not a blog",
      link = "http://b.3cu.eu",
      description = "This is not a blog",
      lastBuildDate = datetime.now(),
      items = map(lambda entry: PyRSS2Gen.RSSItem(title = entry['title'],
                                                  link = "http://b.3cu.eu/entry/" + entry['filename'],
                                                  description = "",
                                                  guid = PyRSS2Gen.Guid("http://b.3cu.eu/entry/" + entry['filename']),
                                                  pubDate = datetime.fromtimestamp(entry['published_date'])), entries))
    return rss.to_xml()

  @cherrypy.expose
  def default(self):
    raise cherrypy.HTTPRedirect("/entries", 301)

class Filtr:

  def __init__(self):
    self._swears = dict({"fuck":"frog", "shit":"shame", "cunt":"cone", "bollock":"balloon","anus":"angus", "rape":"ping", "raping":"damaging", "rapist":"mime", "dick":"baguette","twat":"hobbit", "arse":"frown", "wank":"shuffle", "crap":"craft", "penis":"wand", "cock":"pipe"})

    self._non_swears = frozenset(["cocker","manuscript","manuscripts","drape","draped","draper","draperies","drapers","drapery","drapes","grape","grapefruit","grapes","grapevine","parapet","parapets","psychotherapeutic","scrape","scraped","scraper","scrapers","scrapes","skyscraper","skyscrapers","therapeutic","trapezoid","trapezoidal","trapezoids","physiotherapist","psychotherapist","therapist","therapists","scraping","scrapings","dickens","dicky","wristwatch","wristwatches","arsenal","arsenals","arsenic","coarse","coarsely","coarsen","coarsened","coarseness","coarser","coarsest","hoarse","hoarsely","hoarseness","parse","parsed","parser","parsers","parses","rehearse","rehearsed","rehearser","rehearses","sparse","sparsely","sparseness","sparser","sparsest","unparsed","swank","swanky","scrap","scrapped","scraps","cocked","cocking","cockpit","cockroach","cocks","cocktail","cocktails","cocky","peacock","peacocks","shuttlecock","stopcock","stopcocks","weathercock","weathercocks","woodcock","woodcocks"])

    self._swear_match = re.compile("(?i)" + "|".join(self._swears.keys()))

  def is_swear_word(self, word):
    return (self._swear_match.search(word) is not None) and word.lower() not in self._non_swears

  def un_swear_word(self, word):
    for swear in self._swears.keys():
      word = word.replace(swear, self._swears[swear])
    return word

  def unswear(self, content):
    return ''.join(map(lambda x: x if not self.is_swear_word(x) else self.un_swear_word(x), re.split('(\W)', content)))

