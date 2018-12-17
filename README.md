# HumbleOrganizer

I wrote this script to deal with a problem I had with organizing my Humble Bundle purchases. To get the most of of my purchases (books and DIY stuff, mostly), I would have to download all attached files. In the worst case scenario, this meant that I had to download 

* The book in .mobi
* The book in .epub
* The book in .pdf
* The book in .rc
* Any supplemental materials for the book in .zip format

My original orgizational system was to cluster the books by the bundle they were a part of. However, this presented some problems. If I wanted to look for something specific, I'd have to remember what bundle the book I wanted was a part of, then I'd have to remember the title of the book and any supplemental material that was a part of it. And then there was the issue where sometimes I'd download a duplicate book and it's supplements, which could throw me off when I'm trying to look for something. 

Quite frustrating, no? 

I came up with a new organizational system that would fix most, if not all of these problems, by organizing each folder by the title of the book like so: 

/HumbleBundle/Book_1
  /HumbleBundle/Book_1
    /HumbleBundle/Book_1/EPUB/...
    /HumbleBundle/Book_1/MOBI/...
    /HumbleBundle/Book_1/PDF/...
    /HumbleBundle/Book_1/RC/...
    /HumbleBundle/Book_1/ZIP/...
/HumbleBundle/Book_2
  /HumbleBundle/Book_2
    /HumbleBundle/Book_2/EPUB/...
    /HumbleBundle/Book_2/MOBI/...
    /HumbleBundle/Book_2/PDF/...
    /HumbleBundle/Book_2/RC/...
    /HumbleBundle/Book_2/ZIP/...

And so on. Reorganizing this collection, however, presented several new problems. 
* I knew right away that the collection had duplicates, but it had to flexible enough to accomodate different editions if there were any
* Opening and verifying each file would take time and energy I didn't have 
* There was about ~80 GB of data to go through for this reorganization (when the supplements are counted) 

And that's where this script comes in. I exploited the fact that most of the materials would have a similar naming convention (like, the book.pdf, book.mobi, book.epub, book.rc, book_supplemental.zip), and use hashing to identify duplicate files. 

##HOW TO USE##
To use this script, you'll need Python 3.5+ installed. To run the script, type something like 

python3 organize_folder_by_title.py <source_directory> <destination_directory> 

Please be advised that I did not test for what happens when the source directory is the same as the destination directory, though it shouldn't cause any issue. 
