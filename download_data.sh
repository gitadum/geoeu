#! /bin/bash
CACHE_DATA_DIR=.cache/data
mkdir -p $CACHE_DATA_DIR
cd $CACHE_DATA_DIR
eu_countries=(AUT BEL BGR HRV CYP CZE DNK EST FIN FRA DEU GRC HUN IRL ITA LVA LTU LUX MLT NLD POL PRT ROU SVK SVN ESP SWE)
data_url=https://github.com/wmgeolab/geoBoundaries/raw/main/sourceData/gbOpen
for country in ${eu_countries[@]}; do
    mkdir -p ${country,,}
    cd ${country,,}
    for i in {0..5}; do
        content_zipname=${country}_ADM${i}.zip
        content_url=$data_url/$content_zipname
        if [ -f $content_zipname ]; then
            echo "$content_zipname already exists."
        else
            if curl --head -s --fail $content_url -o /dev/null;
                then
                    echo "downloading $content_zipname"
                    wget $content_url
                else
                    echo "$content_zipname does not exist."
            fi
        fi
        done
        cd ..
    done
cd ../../
echo "Done with the download."
echo "Unzipping the downloaded zips..."
cd $CACHE_DATA_DIR
DEST_DATA_DIR=../../../geoeu/content/data
for dir in $(ls); do
    cd $dir
    mkdir -p $DEST_DATA_DIR/$dir
    for i in {0..5}; do
        zip=${dir^^}_ADM${i}.zip
        if [ -f $zip ]; then
            echo "unzipping $zip..."
            dest_content_dir=$DEST_DATA_DIR/$dir/adm${i}
            mkdir -p $dest_content_dir
            unzip -n $zip -d $dest_content_dir/
            echo "Done."
        else
            :
        fi
    done
    cd ..
done
find ./geoeu/content/data/ -type d -name '__MACOSX' -exec rm -r {} +