import { View, Image, Text, ScrollView } from 'react-native';
import PropTypes from 'prop-types';
import React from 'react';
import info from '../../../assets/info';

import styles from './styles';

const InfoScreen = ({ navigation }) => {
  let imageUri = '';

  if (navigation.state.params) {
    ({ imageUri } = navigation.state.params);
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
   
        {imageUri ? (
          <View>
            <Text style={styles.infoTitle}>
               {info[0].name}
            </Text>

            <Image
              source={{
                uri: imageUri,
              }}
              style={styles.image}
            />
            <Text style={styles.info}>{info[0].info_in_arabic}</Text>
          </View>
        ) : (
          <Text style={styles.notCaptured} >You haven't captured any image yet </Text>
        )}
    </ScrollView>

  );
};

InfoScreen.defaultProps = {
  navigation: {},
};

InfoScreen.propTypes = {
  navigation: PropTypes.shape({}),
};

export default InfoScreen;
