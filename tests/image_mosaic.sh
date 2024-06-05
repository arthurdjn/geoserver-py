#!/bin/bash

##geoserver credentials
layername="polyphemus"
folderpath="/home/adujardin/Documents/Github/geoserver-py/tests/data/polyphemus/"
workspace="demo"
user="admin"
password="geoserver"
geoserverurl="http://localhost:8080/geoserver"
GridSetName="EPSG:3857" #Gridset, used for caching
style1='style1' #style of the layer
maxage=86400 #client-side caching, set to 0 if not wanted


##create workspace
# curl -v -u $user:$password -XPOST -H "Content-type: text/xml" -d "<workspace><name>"$workspace"</name></workspace>" $geoserverurl"/rest/workspaces"


##add external imagemosaic
curl -v -u $user:$password -XPUT -H "Content-type: text/plain" -d "file://"$folderpath"/" $geoserverurl"/rest/workspaces/"$workspace"/coveragestores/"$layername"/external.imagemosaic"


##create layer
# curl -v -u $user:$password -XPUT -H "Content-type: text/xml" -d "<coverage><name>"$layername"</name><id>"$layername"</id><title>"$layername"</title><nativeCRS>EPSG:3857</nativeCRS><srs>EPSG:3857</srs><projectionPolicy>REPROJECT_TO_DECLARED</projectionPolicy><metadata><entry key=\"cacheAgeMax\">"$maxage"</entry><entry key=\"cachingEnabled\">true</entry></metadata><parameters><entry><string>BackgroundValues</string><string>255</string></entry><entry><string>OVERVIEW_POLICY</string><string>QUALITY</string></entry><entry><string>MergeBehavior</string><string>FLAT</string></entry><entry><string>AllowMultithreading</string><string>false</string></entry><entry><string>MaxAllowedTiles</string><string>-1</string></entry><entry><string>ExcessGranuleRemoval</string><string>NONE</string></entry><entry><string>OutputTransparentColor</string><string></string></entry><entry><string>USE_JAI_IMAGEREAD</string><string>true</string></entry><entry><string>Bands</string><string></string></entry><entry><string>RescalePixels</string><string>true</string></entry><entry><string>Filter</string><string></string></entry><entry><string>InputTransparentColor</string><string></string></entry><entry><string>SUGGESTED_TILE_SIZE</string><string>512,512</string></entry><entry><string>Accurate resolution computation</string><string>false</string></entry><entry><string>SORTING</string><string></string></entry><entry><string>FootprintBehavior</string><string>Cut</string></entry></parameters><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>" $geoserverurl"/rest/workspaces/"$workspace"/coveragestores/"$workspace$layername"/coverages/"$layername


# ##apply style
# curl -v -u $user:$password -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>"$style1"</name><workspace>"$workspace"</workspace></defaultStyle></layer>" $geoserverurl"/rest/layers/"$workspace":"$layername""


# ##configure cached layer
# curl -v -u $user:$password -XPOST -H "Content-type: text/xml" -d "<GeoServerLayer><enabled>true</enabled><inMemoryCached>true</inMemoryCached><name>"$workspace":"$layername"</name><mimeFormats><string>image/png8</string></mimeFormats><gridSubsets><gridSubset><gridSetName>"$GridSetName"</gridSetName></gridSubset></gridSubsets><metaWidthHeight><int>4</int><int>4</int></metaWidthHeight><expireCache>0</expireCache><expireClients>"$maxage"</expireClients><parameterFilters><styleParameterFilter><key>STYLES</key><defaultStyle>"$stylename"</defaultStyle></styleParameterFilter></parameterFilters><gutter>5</gutter></GeoServerLayer>" $geoserverurl"/gwc/rest/layers/"$workspace":"$layername""


# ##pre-seed tiles (zoom levels 0-10)
# curl -v -u $user:$password -XPOST -H "Content-type: text/xml" -d "<seedRequest><name>"$workspace":"$layername"</name><gridSetId>"$GridSetName"</gridSetId><zoomStart>0</zoomStart><zoomStop>10</zoomStop><format>image/png8</format><type>seed</type><threadCount>1</threadCount></seedRequest>" $geoserverurl"/gwc/rest/seed/"$workspace":"$layername".xml"