import { ImagePicker } from 'expo';
import PropTypes from 'prop-types';

import { Text, View, Image, TouchableHighlight } from 'react-native';
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
      allowsEditing:true
    });

    const { uri } = result;

    if(!result.cancelled){
    const { navigation } = this.props;

    navigation.navigate('Info', {
      imageUri: uri,
    });}
  };


  pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      base64:true
    });

    const { uri } = result;
 
    if (!result.cancelled) {
      const { navigation } = this.props;

      navigation.navigate('Info', {
        imageUri: uri,
      });
    }
  };

  render() {
    const { imageUri } = this.state;

    return (
      <View style={styles.container}>
        <Text style={styles.welcomeStyles}>Welcome to the Auto Guide app</Text>

        <TouchableHighlight
          style={styles.button}
          onPress={() => ensureCameraPermission(this.openCamera)}
        >
          <Text style={styles.buttonText}>Capture Picture</Text>
        </TouchableHighlight>
        <Text style={styles.separatorText}>OR</Text>
        <TouchableHighlight
          style={styles.button}
          onPress={() => ensureCameraPermission(this.pickImage)}
        >
          <Text style={styles.buttonText}>Pick From Gallery</Text>
        </TouchableHighlight>
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
