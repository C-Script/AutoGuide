import { View, Image,Text } from 'react-native';
import PropTypes from 'prop-types';
import React from 'react';

import styles from './styles';

const InfoScreen = ({ navigation }) => {
  let imageUri = '';

  if (navigation.state.params) {
    ({ imageUri } = navigation.state.params);
  }

  return (
    <View style={styles.container}>
      {imageUri ? (
        <Image
          source={{
            uri: imageUri,
          }}
          style={styles.image}
        />
      ) : <Text>You haven't captured any image yet </Text>}
    </View>
  );
};

InfoScreen.defaultProps = {
  navigation: {},
};

InfoScreen.propTypes = {
  navigation: PropTypes.shape({}),
};

export default InfoScreen;
