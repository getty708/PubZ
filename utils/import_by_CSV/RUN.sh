URL_BASE="http://django:8000/api/rest"
USER="mmde-netwg@mmde-mail.ise.eng.osaka-u.ac.jp"

mode=$1

if [ ${mode} == "auth" ];
then
    URL="${URL_BASE}/api-token-auth/"
    python auth_token.py --url ${URL} -u ${USER}
elif [ ${mode} == "author" ]; then
    CSV="./csv/Pubz_Authors.csv"
    python3 authors.py CSV \
	   --url-base ${URL_BASE} \
	   -u ${USER} \
	   -f ${CSV}
elif [ ${mode} == "book" ]; then
    CSV="./csv/PubZ_Books.csv"
    python3 book.py CSV \
	   --url-base ${URL_BASE} \
	   -u ${USER} \
	   -f ${CSV}
elif [ ${mode} == "bibtex" ]; then
    # CSV="./csv/PubZ_Bibtex.csv"
    # CSV="./csv/bibtex_test.csv"
    CSV="./csv/bibtex_import_new.csv"
    python3 bibtex.py CSV \
	    --url-base ${URL_BASE} \
	    -u ${USER} \
	    -f ${CSV}
elif [ ${mode} == "order" ]; then
    # CSV="./csv/PubZ_Bibtex.csv"
    CSV="./csv/bibtex_import_new.csv"
    #CSV="./csv/bibtex_test.csv"
    python3 author_order.py CSV \
	    --url-base ${URL_BASE} \
	    -u ${USER} \
	    -f ${CSV}
fi
