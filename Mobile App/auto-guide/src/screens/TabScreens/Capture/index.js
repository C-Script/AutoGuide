import { ImagePicker } from 'expo';
import { Text, View, TouchableHighlight } from 'react-native';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import Spinner from 'react-native-loading-spinner-overlay';

import { colors } from '../../../assets/styles/base';
import { ensureCameraPermission } from '../../../helpers/ensurePermissions';
import styles from './styles';

class CaptureScreen extends Component {
  state = {
    uploadingImage: false,
  };

  openCamera = async () => {
    this.setState(() => ({ uploadingImage: true }));
    const result = await ImagePicker.launchCameraAsync({
      base64: true,
    });

    this.setState(() => ({ uploadingImage: false }));

    const { uri } = result;

    if (!result.cancelled) {
      const { navigation } = this.props;

      navigation.navigate('Info', {
        imageUri: uri,
      });
    }
  };

  pickImage = async () => {
    this.setState(() => ({ uploadingImage: true }));

    const result = await ImagePicker.launchImageLibraryAsync({
      base64: true,
    });

    this.setState(() => ({ uploadingImage: false }));

    const { uri } = result;

    if (!result.cancelled) {
      const { navigation } = this.props;

      navigation.navigate('Info', {
        imageUri: uri,
      });
    }
  };

  render() {
    const { uploadingImage } = this.state;

    return (
      <View style={styles.container}>
        <Spinner visible={uploadingImage} color={colors.primary} />

        <Text style={styles.welcomeStyles}>Welcome to the Auto Guide App</Text>

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
