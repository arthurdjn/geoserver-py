<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" version="1.0.0">
  <UserLayer>
    <LayerFeatureConstraints>
      <FeatureTypeConstraint/>
    </LayerFeatureConstraints>
    <UserStyle>
      <Name>raster</Name>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ChannelSelection>
              <GrayChannel>
                <SourceChannelName>1</SourceChannelName>
              </GrayChannel>
            </ChannelSelection>
            <ColorMap type="ramp">
              <ColorMapEntry color="#FFFFFF" quantity="-1" label="label" opacity="0"/>
              <ColorMapEntry color="#0000FF" quantity="0" label="label" opacity="1"/>
              <ColorMapEntry color="#FF0000" quantity="110" label="label" opacity="1"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </UserLayer>
</StyledLayerDescriptor>