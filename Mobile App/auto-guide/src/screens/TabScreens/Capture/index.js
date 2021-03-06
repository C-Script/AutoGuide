import { ImagePicker } from 'expo';
import { Text, View, TouchableHighlight } from 'react-native';
import axios from 'axios';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import Spinner from 'react-native-loading-spinner-overlay';

import { colors } from '../../../assets/styles/base';
import { ensureCameraPermission } from '../../../helpers/ensurePermissions';
import { imageServerUrl } from '../../../constants';
import styles from './styles';

class CaptureScreen extends Component {
  state = {
    uploadingImage: false,
  };

  imagePickerAsync = async (imageType) => {
    let result = '';

    if (imageType === 'cam') {
      result = await ImagePicker.launchCameraAsync({
        base64: true,
      });
    } else {
      result = await ImagePicker.launchImageLibraryAsync({
        base64: true,
      });
    }

    return result;
  };

  pickImage = async (imageType) => {
    this.setState(() => ({ uploadingImage: true }));

    const result = await this.imagePickerAsync(imageType);

    if (!result.cancelled) {
      const { navigation } = this.props;
      const { uri } = result;

      const newImage = new FormData();

      if (uri) {
        const uriParts = uri.split('.');
        const fileType = uriParts[uriParts.length - 1];
        newImage.append('image', {
          uri,
          name: uri.split('/').pop(),
          type: `image/${fileType}`,
        });
      }

      const config = {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      };

      axios
        .post(imageServerUrl, newImage, config)
        .then((res) => {
          const { name: imageName } = res.data;
          console.log(imageName);
          this.setState(() => ({ uploadingImage: false }));
          navigation.navigate('Info', {
            imageUri: uri,
            imageName,
          });
        })
        .catch((err) => {
          this.setState(() => ({ uploadingImage: false }));
          console.log(err);
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
          onPress={() => ensureCameraPermission(() => this.pickImage('cam'))}
        >
          <Text style={styles.buttonText}>Capture Picture</Text>
        </TouchableHighlight>
        <Text style={styles.separatorText}>OR</Text>
        <TouchableHighlight
          style={styles.button}
          onPress={() => ensureCameraPermission(() => this.pickImage('library'))
          }
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
