import { Font } from 'expo';

const loadAllFonts = fonts => fonts.map(font => Font.loadAsync(font));

export const loadFonts = loadAllFonts([
  {
    ralewayRegular: require('./Raleway-Regular.ttf'),
  },
  {
    ralewayBold: require('./Raleway-Bold.ttf'),
  },
  {
    ralewayThin: require('./Raleway-Thin.ttf'),
  },
]);
