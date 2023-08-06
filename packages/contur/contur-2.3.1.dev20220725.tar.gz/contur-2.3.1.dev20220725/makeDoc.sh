#export SPHINX_APIDOC_OPTIONS='members,private-members,undoc-members,show-inheritance';
export SPHINX_APIDOC_OPTIONS='members,undoc-members,show-inheritance'; 
rm -rf doc; sphinx-apidoc -F -o doc/ contur/ -A "David Yallup" -V 1.0 -f --ext-autodoc --ext-doctest --ext-intersphinx --ext-todo -e;

export SPHINX_APIDOC_OPTIONS='members,private-members,undoc-members,show-inheritance';
rm -rf docfull; sphinx-apidoc -F -o docfull/ contur/ -A "David Yallup" -V 1.0 -f --ext-autodoc --ext-doctest --ext-intersphinx --ext-todo -e


#-e to make seperate pages
