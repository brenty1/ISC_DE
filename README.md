To run the program: 
  1. Update in_file variable to the path of your local dataset
  2. Update output file with the directory where you want the output file to land

Design decisions:

I utilized the Pydantic library, as requested. Given that it was a small dataset, it was easier to test possible data inputs. With a larger dataset, I would focus more on versatile and thorough testing to help account for any unexpected values, with more data comes the potential for more bad data to flow through. I would also put a unique constraint on ID in the database table where this data lands.

Similar to what I said above, if the source was a third party API I would focus on more thorough testing. For example, we could test further on date_opened and date_closed by checking if it is an actual date and within a certain range rather than just testing if the field is populated. 

If there were multiple files (part1, part2,...), I think a good check would be to test if they were duplicated for some reason. 

If the source waas a database table, I think you could do your unqiue filter with a sql query. This could be useful for other filters, cleansing, and formatting of dates for example.
