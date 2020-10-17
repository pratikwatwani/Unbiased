mkdir data
cd data/

END=27

for i in $(seq 1 $END)
do 
	if [ ! -f enwiki-latest-stub-meta-history${i}.xml.gz ]; then
	echo 'Downloading file' && aws s3 cp s3://wikiscrape/raw/enwiki-latest-stub-meta-history$i.xml.gz enwiki-latest-stub-meta-history$i.xml.gz && pigz --fast --verbose -d enwiki-latest-stub-meta-history$i.xml.gz && aws s3 sync . s3://wikiscrape/extracted && rm -rf *
        fi
done
