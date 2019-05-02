import { StyleSheet } from 'react-native';
import { colors, fontTypes } from '../../../assets/styles/base';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    borderRadius: 50,
    backgroundColor: colors.secondary,
    padding: 15,
    width: '90%',
  },
  buttonText: {
    fontSize: 20,
    color: colors.white,
    textAlign: 'center',
  },
  separatorText: { margin: 5 },
  welcomeStyles: {
    fontSize: 35,
    marginHorizontal: 5,
    marginBottom: 40,
    textAlign: 'center',
    color: colors.secondary,
    fontFamily: fontTypes.mainBold,
  },
});

export default styles;
