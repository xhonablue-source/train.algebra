import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Calculator, Zap } from 'lucide-react';

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

  // Simple Jet Train Toggle Button
  const JetTrainToggle = ({ type, isActive, onClick, scenario }) => {
    const baseClasses = "relative cursor-pointer transform transition-all duration-500 p-8 rounded-3xl border-4";
    const activeClasses = isActive 
      ? "border-blue-500 bg-blue-50 shadow-2xl scale-105" 
      : "border-gray-300 bg-white hover:border-blue-300 shadow-lg";
    
    return (
      <div className={`${baseClasses} ${activeClasses}`} onClick={onClick}>
        {/* Jet Train Body */}
        <div className="relative flex items-center justify-center">
          <div className={`relative w-40 h-20 rounded-2xl shadow-xl border-4 ${
            type === 'hyperloop' 
              ? 'bg-gradient-to-r from-blue-200 to-blue-400 border-blue-500' 
              : 'bg-gradient-to-r from-purple-200 to-purple-400 border-purple-500'
          }`}>
            
            {/* Train Label */}
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="font-bold text-3xl text-white drop-shadow-lg">
                {scenario === 'same-direction' ? 'SAME →' : 'OPPOSITE ↔'}
              </span>
            </div>
            
            {/* Windows */}
            <div className="absolute top-4 left-6 right-6 flex justify-between">
              <div className="w-5 h-4 bg-white rounded-lg opacity-80"></div>
              <div className="w-5 h-4 bg-white rounded-lg opacity-80"></div>
              <div className="w-5 h-4 bg-white rounded-lg opacity-80"></div>
              <div className="w-5 h-4 bg-white rounded-lg opacity-80"></div>
              <div className="w-5 h-4 bg-white rounded-lg opacity-80"></div>
            </div>
            
            {/* Jet exhaust when active */}
            {isActive && (
              <div className="absolute -right-4 top-1/2 transform -translate-y-1/2">
                <div className="flex flex-col space-y-1">
                  <div className="h-2 w-16 bg-orange-400 animate-pulse rounded-full"></div>
                  <div className="h-2 w-12 bg-yellow-400 animate-pulse rounded-full"></div>
                  <div className="h-2 w-8 bg-red-400 animate-pulse rounded-full"></div>
                </div>
                <div className="absolute top-1/2 transform -translate-y-1/2 right-0 text-3xl animate-bounce">🔥</div>
              </div>
            )}
            
            {/* Magnetic levitation indicators */}
            <div className="absolute -bottom-3 left-8 right-8 flex justify-between">
              <div className="w-8 h-3 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full animate-pulse"></div>
              <div className="w-8 h-3 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full animate-pulse"></div>
              <div className="w-8 h-3 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full animate-pulse"></div>
              <div className="w-8 h-3 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
        
        {/* Scenario info */}
        <div className="relative text-center mt-6">
          <div className={`font-bold text-2xl ${type === 'hyperloop' ? 'text-blue-800' : 'text-purple-800'}`}>
            {scenario === 'same-direction' ? '同方向 Same Direction' : '逆方向 Opposite Directions'}
          </div>
          <div className="text-lg text-gray-600 mt-2">
            {scenario === 'same-direction' ? '→ → (Subtract speeds)' : '→ ← (Add speeds)'}
          </div>
          {scenario === 'opposite-direction' && (
            <div className="mt-3 text-sm text-purple-600 italic bg-purple-50 p-3 rounded-lg">
              💡 Fun Fact: Moving toward each other = ADD speeds!
            </div>
          )}
        </div>
      </div>
    );
  };

  // Simple animated train
  const AnimatedTrain = ({ type, direction, speed, distance, label }) => {
    const trainClasses = `relative w-20 h-10 rounded-lg shadow-lg border-2 ${
      type === 'hyperloop' 
        ? 'bg-gradient-to-r from-blue-400 to-blue-600 border-blue-700' 
        : 'bg-gradient-to-r from-purple-400 to-purple-600 border-purple-700'
    }`;

    return (
      <div className={`flex items-center ${direction === 'left' ? 'flex-row-reverse' : ''}`}>
        <div className="relative">
          <div className={trainClasses}>
            {/* Label */}
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="font-bold text-lg text-white">{label}</span>
            </div>
            
            {/* Jet exhaust */}
            {speed > 0 && (
              <div className={`absolute ${direction === 'left' ? 'right-full mr-1' : 'left-full ml-1'} top-1/2 transform -translate-y-1/2`}>
                <div className="flex flex-col space-y-1">
                  <div className="h-1 w-6 bg-orange-400 animate-pulse"></div>
                  <div className="h-1 w-4 bg-yellow-400 animate-pulse"></div>
                  <div className="h-1 w-3 bg-red-400 animate-pulse"></div>
                </div>
              </div>
            )}
          </div>
          
          <div className={`${direction === 'left' ? 'mr-2' : 'ml-2'} bg-white p-2 rounded-lg shadow-md border text-center`}>
            <div className={`font-bold text-xs ${type === 'hyperloop' ? 'text-blue-600' : 'text-purple-600'}`}>
              {type === 'hyperloop' ? '🚀 Hyperloop' : '⚡ Jet Train'}
            </div>
            <div className="text-xs text-gray-600">{speed} mph</div>
            <div className="text-xs text-gray-500">{distance.toFixed(1)} mi</div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header with your name */}
        <div className="text-center mb-8">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
            🚀 MathCraft: Jet-Powered Train Motion
          </h1>
          <p className="text-2xl font-semibold text-gray-700 mb-2">by Xavier Honablue M.Ed</p>
          <p className="text-xl text-gray-600">Future Transportation Mathematics | Interactive Physics Learning</p>
        </div>

        {/* Interactive Train Toggle Buttons */}
        <div className="bg-white rounded-3xl shadow-2xl p-10 mb-8 border-2 border-gray-200">
          <h2 className="text-4xl font-bold mb-10 text-gray-800 text-center">
            🛸 Click the Jet Trains to Choose Your Scenario!
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
            <JetTrainToggle
              type="hyperloop"
              isActive={scenario === 'same-direction'}
              onClick={() => setScenario('same-direction')}
              scenario="same-direction"
            />

            <JetTrainToggle
              type="maglev"
              isActive={scenario === 'opposite-direction'}
              onClick={() => setScenario('opposite-direction')}
              scenario="opposite-direction"
            />
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
            <Zap className="text-yellow-500" />
            🚀 Jet Train Parameters
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <label className="block text-sm font-bold text-blue-600 mb-2">
                🚀 Hyperloop A Speed: {trainASpeed} mph
              </label>
              <input
                type="range"
                min="100"
                max="500"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full"
              />
              <input
                type="number"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:border-blue-500 focus:outline-none text-lg"
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-bold text-purple-600 mb-2">
                ⚡ Jet Train B Speed: {trainBSpeed} mph
              </label>
              <input
                type="range"
                min="200"
                max="800"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full"
              />
              <input
                type="number"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg focus:border-purple-500 focus:outline-none text-lg"
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-bold text-pink-600 mb-2">
                ⏰ Head Start: {headStart} hours
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
                className="w-full px-4 py-3 border-2 border-pink-300 rounded-lg focus:border-pink-500 focus:outline-none text-lg"
              />
            </div>
          </div>
        </div>

        {/* Animation */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">🎬 Live Animation</h2>
            <div className="flex gap-3">
              <button
                onClick={() => setIsAnimating(!isAnimating)}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg hover:from-blue-700 hover:to-purple-800 transition-all shadow-lg text-lg"
              >
                {isAnimating ? <Pause size={24} /> : <Play size={24} />}
                {isAnimating ? '🛑 Stop' : '🚀 Launch'}
              </button>
              <button
                onClick={resetAnimation}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-lg hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg text-lg"
              >
                <RotateCcw size={24} />
                🔄 Reset
              </button>
            </div>
          </div>

          <div className="relative bg-gradient-to-b from-gray-100 to-gray-200 p-8 rounded-xl border-2 border-gray-300">
            <div className="relative">
              {/* Futuristic Track */}
              <div className="relative w-full h-6 mb-12">
                <div className="w-full h-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg"></div>
                <div className="absolute top-0 left-0 w-full h-1 bg-cyan-400 rounded-full animate-pulse"></div>
                <div className="absolute bottom-0 left-0 w-full h-1 bg-pink-400 rounded-full animate-pulse"></div>
              </div>

              {/* Distance markers */}
              <div className="flex justify-between text-sm text-gray-700 mb-6">
                <span>0 mi</span>
                <span>{Math.round(maxDistance * 0.2)} mi</span>
                <span>{Math.round(maxDistance * 0.4)} mi</span>
                <span>{Math.round(maxDistance * 0.6)} mi</span>
                <span>{Math.round(maxDistance * 0.8)} mi</span>
                <span>{Math.round(maxDistance)} mi</span>
              </div>

              {/* Trains */}
              <div className="relative h-24">
                <div
                  className="absolute transition-all duration-100 ease-linear"
                  style={{ left: `${trainAPos}px`, top: '-60px' }}
                >
                  <AnimatedTrain 
                    type="hyperloop" 
                    direction="right" 
                    speed={trainASpeed} 
                    distance={trainADistance} 
                    label="A"
                  />
                </div>

                <div
                  className="absolute transition-all duration-100 ease-linear"
                  style={{ left: `${trainBPos}px`, top: '20px' }}
                >
                  <AnimatedTrain 
                    type="maglev" 
                    direction={scenario === 'opposite-direction' ? 'left' : 'right'} 
                    speed={trainBSpeed} 
                    distance={trainBDistance} 
                    label="B"
                  />
                </div>

                {meeting && (
                  <div
                    className="absolute top-0 w-2 h-24 bg-gradient-to-b from-green-400 to-green-600 animate-pulse"
                    style={{ left: `${(meeting.distance / maxDistance) * 600}px` }}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                      ⚡ MEET
                    </div>
                  </div>
                )}
              </div>

              {/* Time display */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div className="bg-white p-4 rounded-lg shadow-md">
                  <div className="text-2xl font-bold text-blue-600">{animationTime.toFixed(1)}h</div>
                  <div className="text-sm text-gray-600">Elapsed Time</div>
                </div>
                {meeting && (
                  <>
                    <div className="bg-white p-4 rounded-lg shadow-md">
                      <div className="text-2xl font-bold text-green-600">{meeting.time.toFixed(1)}h</div>
                      <div className="text-sm text-gray-600">Meeting Time</div>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-md">
                      <div className="text-2xl font-bold text-purple-600">
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
        <div className="bg-white rounded-xl shadow-xl p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Calculator className="text-indigo-600" />
              🧮 Mathematical Solution
            </h2>
            <button
              onClick={() => setShowCalculations(!showCalculations)}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-700 text-white rounded-lg hover:from-indigo-700 hover:to-purple-800 transition-all shadow-lg text-lg"
            >
              <Calculator size={20} />
              {showCalculations ? '🙈 Hide' : '🤓 Show'} Calculations
            </button>
          </div>

          {showCalculations && meeting && (
            <div className="space-y-6">
              <div className="bg-gray-50 p-6 rounded-xl">
                <h3 className="font-bold text-xl mb-4">📋 Problem Setup:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <strong>🚀 Hyperloop A:</strong> {trainASpeed} mph, {headStart}-hour head start
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                    <strong>⚡ Jet Train B:</strong> {trainBSpeed} mph, {scenario === 'same-direction' ? 'same direction' : 'opposite direction'}
                  </div>
                </div>
              </div>

              {scenario === 'same-direction' ? (
                <div className="bg-blue-50 p-6 rounded-xl">
                  <h3 className="font-bold text-xl mb-4">🎯 Same Direction Solution:</h3>
                  <div className="space-y-4">
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 1:</strong> Let t = time Train B travels</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 2:</strong> Distance equations:</p>
                      <div className="ml-4 mt-2 font-mono">
                        <p>Train A: {trainASpeed}(t + {headStart})</p>
                        <p>Train B: {trainBSpeed}t</p>
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 3:</strong> Set equal: {trainASpeed}(t + {headStart}) = {trainBSpeed}t</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg">
                      <p><strong>Step 4:</strong> Solve: t = {meeting.time.toFixed(2)} hours</p>
                    </div>
                    <div className="bg-green-100 p-4 rounded-lg">
                      <p className="font-bold text-green-800">
                        ✅ Answer: Train B catches Train A after {meeting.time.toFixed(1)} hours
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-purple-50 p-6 rounded-xl">
                  <h3 className="font-bold text-xl mb-4">🎯 Opposite Direction Solution:</h3>
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
                    <div className="bg-green-100 p-4 rounded-lg">
                      <p className="font-bold text-green-800">
                        ✅ Answer: Trains meet after {meeting.time.toFixed(1)} hours
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div className="bg-yellow-50 p-6 rounded-xl">
                <h3 className="font-bold text-xl mb-4">🧠 Key Concepts:</h3>
                <ul className="space-y-2">
                  <li>• <strong>Same direction:</strong> Subtract speeds (relative speed)</li>
                  <li>• <strong>Opposite directions:</strong> Add speeds (combined approach)</li>
                  <li>• <strong>Distance = Speed × Time</strong> for each train</li>
                  <li>• Meeting occurs when distances are equal</li>
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
