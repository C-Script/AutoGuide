import { ImagePicker } from 'expo';
import PropTypes from 'prop-types';

import {
  Text, View, Button, Image,
} from 'react-native';
import React, { Component } from 'react';

import { ensureCameraPermission } from '../../../helpers/ensurePermissions';
import styles from './styles';

class CaptureScreen extends Component {
  state = {
    imageUri: '',
  };

  openCamera = async () => {
    const result = await ImagePicker.launchCameraAsync({
      base64: true,
    });

    const { uri } = result;

    const { navigation } = this.props;

    navigation.navigate('Info', {
      imageUri: uri,
    });
  };

  render() {
    const { imageUri } = this.state;

    return (
      <View style={styles.container}>
        <Text>Capture</Text>
        <Button
          title="Take a pic"
          onPress={() => ensureCameraPermission(this.openCamera)}
        />
        {imageUri ? (
          <Image
            source={{
              uri: imageUri,
            }}
            style={{ width: 50, height: 50 }}
          />
        ) : null}
      </View>
    );
  }
}

CaptureScreen.defaultProps = {
  navigation: {},
};

CaptureScreen.propTypes = {
  navigation: PropTypes.shape({}),
};

export default CaptureScreen;
