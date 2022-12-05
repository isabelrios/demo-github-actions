echo "Script to find if JSON files are different"

#if this command is empty, there are no differences
generatedFiles=(content-track-digest256.json base-fingerprinting-track.json)
odlFiles=(content-track-digest256-*.json base-fingerprinting-track-*.json)

createNewVersion=false

for ((i=0; i<${#generatedFiles[@]}; i++)); do
    echo "loop $i"
    #do something to each element of array
    echo "${generatedFiles[$i]}" "${odlFiles[$i]]}"
    echo "DIFF"
    diff --unified "${generatedFiles[$i]}" "${odlFiles[$i]}"
    if [ ! -z "$(diff --unified "${generatedFiles[$i]}" "${odlFiles[$i]}")" ]
    then
        echo "there are changes in files"
        echo "loop $i"
        createNewVersion=true
    else
        echo "There are NO changes in files"
    fi
done

if [ "$createNewVersion" = true ]
then
    echo "Read version folder"
    version=`cat version.txt`
    echo $version
    echo "Create version folder +1"
    mkdir "shavar_version_$(( ${version} + 1))"
    echo "shavar_version_$(( ${version} + 1))"

    echo "Copy all generated Files into a new folder +1"
    for ((i=0; i<${#generatedFiles[@]}; i++)); do
        cp ${generatedFiles[$i]} "shavar_version_$(( ${version} + 1))"
        echo "Files copied to the new release folder"
    done
    sed -i -e "s/$version/$(( ${version} + 1))/g" version.txt
fi
