import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Calculator } from 'lucide-react';

const TrainCalculator = () => {
  const [scenario, setScenario] = useState('same-direction');
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationTime, setAnimationTime] = useState(0);
  const [trainASpeed, setTrainASpeed] = useState(40);
  const [trainBSpeed, setTrainBSpeed] = useState(60);
  const [headStart, setHeadStart] = useState(2);
  const [showCalculations, setShowCalculations] = useState(false);
  const animationRef = useRef();

  const calculateMeeting = () => {
    if (scenario === 'same-direction') {
      if (trainBSpeed <= trainASpeed) return null;
      const meetingTime = (trainASpeed * headStart) / (trainBSpeed - trainASpeed);
      const meetingDistance = trainBSpeed * meetingTime;
      return { 
        time: meetingTime, 
        distance: meetingDistance,
        trainADistance: trainASpeed * (meetingTime + headStart),
        trainBDistance: trainBSpeed * meetingTime 
      };
    } else {
      const combinedSpeed = trainASpeed + trainBSpeed;
      const initialDistance = trainASpeed * headStart;
      const meetingTime = initialDistance / combinedSpeed;
      const meetingDistance = trainASpeed * (headStart + meetingTime);
      return { 
        time: meetingTime, 
        distance: meetingDistance,
        trainADistance: trainASpeed * (headStart + meetingTime),
        trainBDistance: trainBSpeed * meetingTime
      };
    }
  };

  const meeting = calculateMeeting();

  useEffect(() => {
    if (isAnimating) {
      const startTime = Date.now();
      const animate = () => {
        const elapsed = (Date.now() - startTime) / 1000;
        setAnimationTime(elapsed);
        
        if (meeting && elapsed < meeting.time + 3) {
          animationRef.current = requestAnimationFrame(animate);
        } else {
          setIsAnimating(false);
        }
      };
      animationRef.current = requestAnimationFrame(animate);
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isAnimating, meeting]);

  const resetAnimation = () => {
    setIsAnimating(false);
    setAnimationTime(0);
  };

  const getTrainPositions = () => {
    const trackWidth = 600;
    const maxDistance = meeting ? Math.max(meeting.distance * 1.3, 300) : 300;
    
    let trainADistance, trainBDistance;
    
    if (scenario === 'same-direction') {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    } else {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    }
    
    const trainAPos = Math.min((trainADistance / maxDistance) * trackWidth, trackWidth - 80);
    let trainBPos;
    
    if (scenario === 'same-direction') {
      trainBPos = Math.min((trainBDistance / maxDistance) * trackWidth, trackWidth - 80);
    } else {
      trainBPos = Math.max(trackWidth - 80 - (trainBDistance / maxDistance) * trackWidth, 0);
    }
    
    return { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance };
  };

  const { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance } = getTrainPositions();

  return (
    <div className="min-h-screen bg-blue-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-blue-600 mb-4">
            MathCraft: Jet Train Motion
          </h1>
          <p className="text-2xl font-semibold text-gray-700 mb-2">by Xavier Honablue M.Ed</p>
          <p className="text-xl text-gray-600">Future Transportation Mathematics</p>
        </div>

        {/* Interactive Train Toggle Buttons */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-3xl font-bold mb-8 text-center">
            Click the Trains to Choose Your Scenario!
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Same Direction Toggle */}
            <div 
              className={`cursor-pointer p-8 rounded-lg border-4 transition-all ${
                scenario === 'same-direction' 
                  ? 'border-blue-500 bg-blue-50 shadow-lg transform scale-105' 
                  : 'border-gray-300 bg-white hover:border-blue-300'
              }`}
              onClick={() => setScenario('same-direction')}
            >
              <div className="text-center">
                <div className="text-8xl mb-6">
                  <span className="inline-block">🚂</span>
                  <span className="mx-4">→</span>
                  <span className="inline-block">🚂</span>
                </div>
                <h3 className="text-2xl font-bold text-blue-800 mb-3">Same Direction</h3>
                <p className="text-gray-600 mb-3">Faster train catches slower train</p>
                <p className="text-blue-600 font-mono text-lg">SUBTRACT speeds</p>
                {scenario === 'same-direction' && (
                  <div className="mt-4 text-orange-500 animate-pulse text-xl font-bold">
                    ★ SELECTED ★
                  </div>
                )}
              </div>
            </div>

            {/* Opposite Direction Toggle */}
            <div 
              className={`cursor-pointer p-8 rounded-lg border-4 transition-all ${
                scenario === 'opposite-direction' 
                  ? 'border-purple-500 bg-purple-50 shadow-lg transform scale-105' 
                  : 'border-gray-300 bg-white hover:border-purple-300'
              }`}
              onClick={() => setScenario('opposite-direction')}
            >
              <div className="text-center">
                <div className="text-8xl mb-6">
                  <span className="inline-block">🚂</span>
                  <span className="mx-4">↔</span>
                  <span className="inline-block">🚂</span>
                </div>
                <h3 className="text-2xl font-bold text-purple-800 mb-3">Opposite Directions</h3>
                <p className="text-gray-600 mb-3">Trains move toward each other</p>
                <p className="text-purple-600 font-mono text-lg">ADD speeds</p>
                {scenario === 'opposite-direction' && (
                  <div className="mt-4 text-orange-500 animate-pulse text-xl font-bold">
                    ★ SELECTED ★
                  </div>
                )}
                {scenario === 'opposite-direction' && (
                  <div className="mt-4 text-sm text-purple-600 italic bg-purple-100 p-3 rounded">
                    Fun Fact: Moving toward each other = ADD speeds!
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">
            Train Parameters
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <label className="block text-sm font-bold text-blue-600 mb-2">
                Train A Speed: {trainASpeed} mph
              </label>
              <input
                type="range"
                min="20"
                max="200"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full"
              />
              <input
                type="number"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg text-lg"
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-bold text-purple-600 mb-2">
                Train B Speed: {trainBSpeed} mph
              </label>
              <input
                type="range"
                min="30"
                max="300"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full"
              />
              <input
                type="number"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg text-lg"
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-bold text-green-600 mb-2">
                Head Start: {headStart} hours
              </label>
              <input
                type="range"
                min="0.5"
                max="5"
                step="0.5"
                value={headStart}
                onChange={(e) => setHeadStart(Number(e.target.value))}
                className="w-full"
              />
              <input
                type="number"
                value={headStart}
                onChange={(e) => setHeadStart(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-green-300 rounded-lg text-lg"
              />
            </div>
          </div>
        </div>

        {/* Animation */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Live Animation</h2>
            <div className="flex gap-3">
              <button
                onClick={() => setIsAnimating(!isAnimating)}
                className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-semibold"
              >
                {isAnimating ? <Pause size={24} /> : <Play size={24} />}
                {isAnimating ? 'STOP' : 'START'}
              </button>
              <button
                onClick={resetAnimation}
                className="flex items-center gap-2 px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 text-lg font-semibold"
              >
                <RotateCcw size={24} />
                RESET
              </button>
            </div>
          </div>

          <div className="bg-gray-100 p-8 rounded-lg">
            <div className="relative">
              {/* Track */}
              <div className="w-full h-6 bg-gray-600 rounded-lg mb-8 relative">
                <div className="absolute top-1 left-0 w-full h-1 bg-gray-800"></div>
                <div className="absolute bottom-1 left-0 w-full h-1 bg-gray-800"></div>
              </div>

              {/* Distance markers */}
              <div className="flex justify-between text-sm text-gray-700 mb-6 font-mono">
                <span>0 mi</span>
                <span>{Math.round(maxDistance * 0.2)} mi</span>
                <span>{Math.round(maxDistance * 0.4)} mi</span>
                <span>{Math.round(maxDistance * 0.6)} mi</span>
                <span>{Math.round(maxDistance * 0.8)} mi</span>
                <span>{Math.round(maxDistance)} mi</span>
              </div>

              {/* Trains */}
              <div className="relative h-24">
                {/* Train A */}
                <div
                  className="absolute transition-all duration-100"
                  style={{ left: `${trainAPos}px`, top: '-50px' }}
                >
                  <div className="flex items-center">
                    <div className="text-5xl">🚂</div>
                    <div className="ml-3 bg-white p-3 rounded-lg shadow-md border-2 border-blue-300">
                      <div className="font-bold text-blue-600">Train A</div>
                      <div className="text-sm text-gray-600">{trainASpeed} mph</div>
                      <div className="text-xs text-gray-500">{trainADistance.toFixed(1)} miles</div>
                    </div>
                  </div>
                </div>

                {/* Train B */}
                <div
                  className="absolute transition-all duration-100"
                  style={{ 
                    left: `${trainBPos}px`, 
                    top: '20px',
                    transform: scenario === 'opposite-direction' ? 'scaleX(-1)' : 'scaleX(1)'
                  }}
                >
                  <div className="flex items-center">
                    <div className="text-5xl">🚄</div>
                    <div className={`ml-3 bg-white p-3 rounded-lg shadow-md border-2 border-purple-300 ${scenario === 'opposite-direction' ? 'transform scale-x-[-1]' : ''}`}>
                      <div className="font-bold text-purple-600">Train B</div>
                      <div className="text-sm text-gray-600">{trainBSpeed} mph</div>
                      <div className="text-xs text-gray-500">{trainBDistance.toFixed(1)} miles</div>
                    </div>
                  </div>
                </div>

                {/* Meeting point */}
                {meeting && (
                  <div
                    className="absolute top-0 w-2 h-24 bg-green-500 animate-pulse rounded-full"
                    style={{ left: `${(meeting.distance / maxDistance) * 600}px` }}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-3 py-2 rounded-full text-sm font-bold">
                      MEET HERE
                    </div>
                  </div>
                )}
              </div>

              {/* Time display */}
              <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
                  <div className="text-3xl font-bold text-blue-600">{animationTime.toFixed(1)}h</div>
                  <div className="text-sm text-gray-600">Time Elapsed</div>
                </div>
                {meeting && (
                  <>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
                      <div className="text-3xl font-bold text-green-600">{meeting.time.toFixed(1)}h</div>
                      <div className="text-sm text-gray-600">Meeting Time</div>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-purple-500">
                      <div className="text-3xl font-bold text-purple-600">
                        {scenario === 'same-direction' ? trainBSpeed - trainASpeed : trainASpeed + trainBSpeed}
                      </div>
                      <div className="text-sm text-gray-600">
                        {scenario === 'same-direction' ? 'Relative Speed' : 'Combined Speed'} (mph)
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Calculator */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Calculator className="text-indigo-600" />
              Mathematical Solution
            </h2>
            <button
              onClick={() => setShowCalculations(!showCalculations)}
              className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-lg font-semibold"
            >
              <Calculator size={20} />
              {showCalculations ? 'HIDE' : 'SHOW'} Math
            </button>
          </div>

          {showCalculations && meeting && (
            <div className="space-y-6">
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="font-bold text-xl mb-4">Problem Setup:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <strong>Train A:</strong> {trainASpeed} mph, {headStart}-hour head start
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                    <strong>Train B:</strong> {trainBSpeed} mph, {scenario === 'same-direction' ? 'same direction' : 'opposite direction'}
                  </div>
                </div>
              </div>

              {scenario === 'same-direction' ? (
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="font-bold text-xl mb-4">Same Direction Solution:</h3>
                  <div className="space-y-4">
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 1:</strong> Let t = time Train B travels</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 2:</strong> Distance equations:</p>
                      <div className="ml-4 mt-2 font-mono text-blue-700">
                        <p>Train A: {trainASpeed} × (t + {headStart})</p>
                        <p>Train B: {trainBSpeed} × t</p>
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 3:</strong> Set equal and solve:</p>
                      <p className="font-mono ml-4 text-blue-700">t = {meeting.time.toFixed(2)} hours</p>
                    </div>
                    <div className="bg-green-100 p-4 rounded-lg border-2 border-green-300">
                      <p className="font-bold text-green-800 text-lg">
                        ANSWER: Train B catches Train A after {meeting.time.toFixed(1)} hours
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-purple-50 p-6 rounded-lg">
                  <h3 className="font-bold text-xl mb-4">Opposite Direction Solution:</h3>
                  <div className="space-y-4">
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 1:</strong> Initial separation = {trainASpeed * headStart} miles</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 2:</strong> Combined speed = {trainASpeed + trainBSpeed} mph</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 3:</strong> Time = {meeting.time.toFixed(2)} hours</p>
                    </div>
                    <div className="bg-green-100 p-4 rounded-lg border-2 border-green-300">
                      <p className="font-bold text-green-800 text-lg">
                        ANSWER: Trains meet after {meeting.time.toFixed(1)} hours
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div className="bg-yellow-50 p-6 rounded-lg border-2 border-yellow-300">
                <h3 className="font-bold text-xl mb-4">Key Mathematical Concepts:</h3>
                <ul className="space-y-2 text-lg">
                  <li><strong>Same direction:</strong> Subtract speeds (relative speed)</li>
                  <li><strong>Opposite directions:</strong> Add speeds (combined approach)</li>
                  <li><strong>Distance = Speed × Time</strong> for each train</li>
                  <li><strong>Meeting occurs when distances are equal</strong></li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TrainCalculator;
