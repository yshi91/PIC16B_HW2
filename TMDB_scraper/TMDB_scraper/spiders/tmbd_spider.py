# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    # we will start with the movie Train to Busan
    start_urls = ['https://www.themoviedb.org/movie/396535']
    
    
    def parse(self, response):
        '''
        we start on the movie page, and then navigate to the Full Cast & Crew page
        '''
        
        # we need to go the next page which is https://www.themoviedb.org/movie/396535/cast
        
        # use the response.css method to get the link for next page
        next_page = response.css("p.new_button a::attr(href)").get()
        
        # get the full url link of the next page
        next_page = response.urljoin(next_page)
        
        # parse_full_credits(self,response) should be called next by yielding the scrapy.Request
        yield scrapy.Request(next_page, callback = self.parse_full_credits)

        
        
        
    def parse_full_credits(self, response):
        '''
        this function gets all the links for the cast of the movie
        '''
        
        # using a for loop to get all the links for actors
        cast_links = [elem.attrib["href"] for elem in response.css("ol.people.credits div.info a")]
        
        # yield all the full links of the actor's page we want to go and call teh parse_actor_page function
        for link in cast_links:
            yield scrapy.Request(response.urljoin(link), callback = self.parse_actor_page)
            
    
    def parse_actor_page(self, response):
        '''
        get the dictionary of the movies or TV shows that include the corresponding actor
        '''
        
        # get the name of the actor
        actor_name = response.css("div.title h2.title a::text").get()
        
        # get the list of all the acting the actor did
        acting_list = response.css("a.tooltip bdi::text").getall()
        
        # yield the name of the actor along with their acting of movies or TV shows
        for acting in acting_list:
            yield {"actor name": actor_name,
                   "acting": acting
                  }
        # this is the end of the code
        
