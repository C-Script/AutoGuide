import { StyleSheet } from 'react-native';

import { colors, fontTypes } from '../../../assets/styles/base';

const styles = StyleSheet.create({
  image: {
    width: 200,
    height: 330,
    borderRadius: 10,
    borderWidth: 3,
    borderColor: colors.white,
    alignSelf: 'center',
    marginBottom: 5,
  },
  info: {
    marginHorizontal: 10,
    textAlign: 'center',
    fontSize: 18,
    marginBottom: 10,
  },
  infoTitle: {
    marginVertical: 5,
    textAlign: 'center',
    fontSize: 30,
    fontFamily: fontTypes.mainBold,
  },
  notCaptured: {
    alignSelf: 'center',
    marginTop: 50,
    fontFamily: fontTypes.mainBold,
  },
});

export default styles;
