from pattern.web import Twitter, plaintext
from pattern.en import parsetree
from pattern.graph  import Graph
from pattern.search import search
import argparse

def get_pattern_data(search_param):
   
   twitter = Twitter(language='en') 
   
   for tweet in twitter.search(search_param, cached=True):
      print(plaintext(tweet.text).encode('ascii', 'ignore').decode('utf-8'))
   

   g = Graph()
   for i in range(10):
      for result in twitter.search(search_param, start=i+1,count=50):
         s = result.text.lower() 
         s = plaintext(s)
         s = parsetree(s)
         p = '{NP} (VP) ' +search_param+ ' {NP}'
         for m in search(p, s):
            x = m.group(1).string # NP left
            y = m.group(2).string # NP right
            if x not in g:
               g.add_node(x)
               if y not in g:
                  g.add_node(y)
               g.add_edge(g[x], g[y], stroke=(0,0,0,0.75)) # R,G,B,A

   #if len(g)>0:   
   #   g = g.split()[0] # Largest subgraph.

   for n in g.sorted()[:40]: # Sort by Node.weight.
      n.fill = (0, 0.5, 1, 0.75 * n.weight)

   g.export('data', directed=False, weighted=0.6)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Uses pattern for search.', prog='pattern_data.py', epilog="", add_help=False)
   # Adding the main options
   general = parser.add_mutually_exclusive_group(required=True)
   general.add_argument('-s', '--search', metavar='<search>', action='store', help='query to be resolved.')
   args = parser.parse_args()       
        
        
   get_pattern_data(args.search)