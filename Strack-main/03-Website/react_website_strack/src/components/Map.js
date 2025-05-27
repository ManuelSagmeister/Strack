import React from 'react'
import { GoogleMap, useJsApiLoader } from '@react-google-maps/api';
import { Marker } from '@react-google-maps/api';


const locations = [{
    lat: 47.1885368,
    lng: 9.7166329
  },
  {
    lat: 37.672,
    lng: -122.219
  },
  {
    lat: 37.832,
    lng: -122.424
  }];

const containerStyle = {
  width: '100vw',
  height: '100vh'
};

const center = {
  lat: 47.1885368,
  lng: 9.7166329
};

function MyComponent() {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: "AIzaSyC9uc0hQgm-jQJBa2HfCy3s1vcmuHW265Y"
  })

  const [map, setMap] = React.useState(null)

  const onLoad = React.useCallback(function callback(map) {
    const bounds = new window.google.maps.LatLngBounds(center);
    
    setMap(map)
  }, [])

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null)
  }, [])

  return isLoaded ? (
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={15}
        onLoad={onLoad}
        onUnmount={onUnmount}
        options={{ mapTypeId: 'satellite' }}
        
      >
         {/* Child components, such as markers, info windows, etc. */
          <Marker
          
          onLoad={onLoad}
          position={locations[0]}
          label=""
          />
         
         }
          
        
        <></>
      </GoogleMap>
  ) : <></>
  
}

export default React.memo(MyComponent)

