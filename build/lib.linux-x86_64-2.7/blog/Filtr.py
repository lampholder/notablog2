# This Python file uses the following encoding: utf-8
import re

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
    return ''.join(map(lambda x: x if not self._is_swear_word(x) else self._un_swear_word(x), re.split('(\W)', content)))
