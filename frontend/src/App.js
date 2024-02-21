
import './App.css';
import Header from './components/Header';
import LeafletMap from './components/LeafletMap';
import WeatherDataList from './components/WeatherDataList';

function App() {
  return (
    <div className="App">
      <Header />
      Map
      <LeafletMap />
      Project
      <WeatherDataList />
    </div>
  );
}

export default App;
