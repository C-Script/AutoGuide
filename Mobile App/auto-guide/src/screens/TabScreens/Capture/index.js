import { ImagePicker } from 'expo';
import { Text, View, Button } from 'react-native';
import React from 'react';

import { ensureCameraPermission } from '../../../helpers/ensurePermissions';
import styles from './styles';

const CaptureScreen = () => {
  const openCamera = async () => {
    const result = await ImagePicker.launchCameraAsync({});

    const { uri } = result;
    console.log(uri);
  };

  return (
    <View style={styles.container}>
      <Text>Capture</Text>
      <Button
        title="Take a pic"
        onPress={() => ensureCameraPermission(openCamera)}
      />
    </View>
  );
};

export default CaptureScreen;
