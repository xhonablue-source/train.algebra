import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Calculator, Train, BookOpen, Zap } from 'lucide-react';

const MathCraftTrainApp = () => {
  const [scenario, setScenario] = useState('same-direction');
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationTime, setAnimationTime] = useState(0);
  const [trainASpeed, setTrainASpeed] = useState(40);
  const [trainBSpeed, setTrainBSpeed] = useState(60);
  const [headStart, setHeadStart] = useState(2);
  const [showCalculations, setShowCalculations] = useState(false);
  const [showMathTutorial, setShowMathTutorial] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const animationRef = useRef();

  // Calculate meeting time and position
  const calculateMeeting = () => {
    if (scenario === 'same-direction') {
      if (trainBSpeed <= trainASpeed) return null; // B must be faster to catch up
      const meetingTime = (trainASpeed * headStart) / (trainBSpeed - trainASpeed);
      const meetingDistance = trainBSpeed * meetingTime;
      return { 
        time: meetingTime, 
        distance: meetingDistance,
        trainADistance: trainASpeed * (meetingTime + headStart),
        trainBDistance: trainBSpeed * meetingTime 
      };
    } else {
      // Opposite directions
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

  // Animation logic with smooth sliding
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
    setCurrentStep(0);
  };

  // Calculate train positions for smooth animation
  const getTrainPositions = () => {
    const trackWidth = 700;
    const maxDistance = meeting ? Math.max(meeting.distance * 1.3, 300) : 300;
    
    let trainADistance, trainBDistance;
    
    if (scenario === 'same-direction') {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    } else {
      trainADistance = trainASpeed * (animationTime + headStart);
      trainBDistance = animationTime > 0 ? trainBSpeed * animationTime : 0;
    }
    
    const trainAPos = Math.min((trainADistance / maxDistance) * trackWidth, trackWidth - 60);
    let trainBPos;
    
    if (scenario === 'same-direction') {
      trainBPos = Math.min((trainBDistance / maxDistance) * trackWidth, trackWidth - 60);
    } else {
      trainBPos = Math.max(trackWidth - 60 - (trainBDistance / maxDistance) * trackWidth, 0);
    }
    
    return { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance };
  };

  const { trainAPos, trainBPos, maxDistance, trainADistance, trainBDistance } = getTrainPositions();

  // Math tutorial steps
  const getMathSteps = () => {
    if (scenario === 'same-direction') {
      return [
        {
          title: "Problem Setup",
          content: `Train A: ${trainASpeed} mph, ${headStart} hour head start\nTrain B: ${trainBSpeed} mph, starts later`,
          visual: "Both trains move in same direction →"
        },
        {
          title: "Key Insight",
          content: `Since both move same direction, we use RELATIVE SPEED\nRelative Speed = Faster Speed - Slower Speed = ${trainBSpeed} - ${trainASpeed} = ${trainBSpeed - trainASpeed} mph`,
          visual: "Train B gains on Train A at " + (trainBSpeed - trainASpeed) + " mph"
        },
        {
          title: "Initial Gap",
          content: `Train A's head start creates initial gap:\nGap = Speed × Time = ${trainASpeed} × ${headStart} = ${trainASpeed * headStart} miles`,
          visual: "Train A is " + (trainASpeed * headStart) + " miles ahead when B starts"
        },
        {
          title: "Time to Close Gap",
          content: `Time = Distance ÷ Speed\nTime = ${trainASpeed * headStart} ÷ ${trainBSpeed - trainASpeed} = ${meeting?.time.toFixed(2)} hours`,
          visual: "Train B needs " + meeting?.time.toFixed(2) + " hours to catch up"
        }
      ];
    } else {
      return [
        {
          title: "Problem Setup",
          content: `Train A: ${trainASpeed} mph, ${headStart} hour head start →\nTrain B: ${trainBSpeed} mph, moves toward A ←`,
          visual: "Trains move toward each other"
        },
        {
          title: "Key Insight",
          content: `Moving toward each other = ADD SPEEDS\nCombined Speed = ${trainASpeed} + ${trainBSpeed} = ${trainASpeed + trainBSpeed} mph`,
          visual: "They approach at " + (trainASpeed + trainBSpeed) + " mph combined"
        },
        {
          title: "Initial Separation",
          content: `When B starts, they are separated by:\nSeparation = ${trainASpeed} × ${headStart} = ${trainASpeed * headStart} miles`,
          visual: "Initial gap: " + (trainASpeed * headStart) + " miles"
        },
        {
          title: "Time to Meet",
          content: `Time = Distance ÷ Combined Speed\nTime = ${trainASpeed * headStart} ÷ ${trainASpeed + trainBSpeed} = ${meeting?.time.toFixed(2)} hours`,
          visual: "They meet in " + meeting?.time.toFixed(2) + " hours"
        }
      ];
    }
  };

  const mathSteps = getMathSteps();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3 flex items-center justify-center gap-3">
            <Train className="text-blue-600" size={48} />
            MathCraft: Interactive Train Motion
          </h1>
          <p className="text-xl text-gray-600">Master relative motion with visual mathematics</p>
        </div>

        {/* Scenario Toggle */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Choose Your Scenario</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className={`flex items-center space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-all ${
              scenario === 'same-direction' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
            }`}>
              <input
                type="radio"
                name="scenario"
                value="same-direction"
                checked={scenario === 'same-direction'}
                onChange={(e) => setScenario(e.target.value)}
                className="text-blue-600 scale-125"
              />
              <div>
                <div className="font-semibold text-lg">Same Direction</div>
                <div className="text-gray-600">Faster train catches slower train</div>
                <div className="text-sm text-blue-600">→ → (Subtract speeds)</div>
              </div>
            </label>
            <label className={`flex items-center space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-all ${
              scenario === 'opposite-direction' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-purple-300'
            }`}>
              <input
                type="radio"
                name="scenario"
                value="opposite-direction"
                checked={scenario === 'opposite-direction'}
                onChange={(e) => setScenario(e.target.value)}
                className="text-purple-600 scale-125"
              />
              <div>
                <div className="font-semibold text-lg">Opposite Directions</div>
                <div className="text-gray-600">Trains move toward each other</div>
                <div className="text-sm text-purple-600">→ ← (Add speeds)</div>
              </div>
            </label>
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
            <Zap className="text-yellow-500" />
            Train Parameters
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="block text-sm font-bold text-red-600 mb-2">
                🚂 Train A Speed: {trainASpeed} mph
              </label>
              <input
                type="range"
                min="10"
                max="100"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full h-3 bg-red-200 rounded-lg appearance-none cursor-pointer slider-red"
              />
              <input
                type="number"
                value={trainASpeed}
                onChange={(e) => setTrainASpeed(Number(e.target.value))}
                className="w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:border-red-500 focus:outline-none"
                min="1"
                max="150"
              />
            </div>
            <div className="space-y-2">
              <label className="block text-sm font-bold text-blue-600 mb-2">
                🚂 Train B Speed: {trainBSpeed} mph
              </label>
              <input
                type="range"
                min="10"
                max="100"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full h-3 bg-blue-200 rounded-lg appearance-none cursor-pointer slider-blue"
              />
              <input
                type="number"
                value={trainBSpeed}
                onChange={(e) => setTrainBSpeed(Number(e.target.value))}
                className="w-full px-3 py-2 border-2 border-blue-300 rounded-lg focus:border-blue-500 focus:outline-none"
                min="1"
                max="150"
              />
            </div>
            <div className="space-y-2">
              <label className="block text-sm font-bold text-green-600 mb-2">
                ⏰ Head Start: {headStart} hours
              </label>
              <input
                type="range"
                min="0.5"
                max="10"
                step="0.5"
                value={headStart}
                onChange={(e) => setHeadStart(Number(e.target.value))}
                className="w-full h-3 bg-green-200 rounded-lg appearance-none cursor-pointer slider-green"
              />
              <input
                type="number"
                value={headStart}
                onChange={(e) => setHeadStart(Number(e.target.value))}
                className="w-full px-3 py-2 border-2 border-green-300 rounded-lg focus:border-green-500 focus:outline-none"
                min="0"
                max="20"
                step="0.5"
              />
            </div>
          </div>
        </div>

        {/* Math Tutorial Section */}
        {showMathTutorial && (
          <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl shadow-xl p-6 mb-6 border-2 border-yellow-200">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-orange-800 flex items-center gap-2">
                <BookOpen className="text-orange-600" />
                Visual Math Tutorial
              </h2>
              <button
                onClick={() => setShowMathTutorial(!showMathTutorial)}
                className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
              >
                Hide Tutorial
              </button>
            </div>
            
            {meeting && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  {mathSteps.map((step, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                        currentStep === index 
                          ? 'border-orange-400 bg-orange-100' 
                          : 'border-orange-200 bg-white hover:border-orange-300'
                      }`}
                      onClick={() => setCurrentStep(index)}
                    >
                      <h3 className="font-bold text-lg text-orange-800">
                        Step {index + 1}: {step.title}
                      </h3>
                      <p className="text-gray-700 whitespace-pre-line text-sm mt-2">
                        {step.content}
                      </p>
                    </div>
                  ))}
                </div>
                
                <div className="bg-white p-6 rounded-lg border-2 border-orange-200">
                  <h3 className="font-bold text-xl text-orange-800 mb-4">
                    {mathSteps[currentStep]?.title}
                  </h3>
                  <div className="text-6xl text-center mb-4">
                    {scenario === 'same-direction' ? '🚂→  🚂→' : '🚂→  ←🚂'}
                  </div>
                  <div className="text-center text-lg font-medium text-gray-700 bg-orange-50 p-4 rounded-lg">
                    {mathSteps[currentStep]?.visual}
                  </div>
                  
                  {/* Real-time values */}
                  <div className="mt-4 space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Train A Distance:</span>
                      <span className="font-mono">{trainADistance.toFixed(1)} mi</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Train B Distance:</span>
                      <span className="font-mono">{trainBDistance.toFixed(1)} mi</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Time Elapsed:</span>
                      <span className="font-mono">{animationTime.toFixed(1)} hrs</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Animation Controls */}
        <div className="bg-white rounded-xl shadow-xl p-6 mb-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800">🎬 Live Animation</h2>
            <div className="flex gap-3">
              <button
                onClick={() => setIsAnimating(!isAnimating)}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg"
              >
                {isAnimating ? <Pause size={20} /> : <Play size={20} />}
                {isAnimating ? 'Pause' : 'Play'}
              </button>
              <button
                onClick={resetAnimation}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-lg hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg"
              >
                <RotateCcw size={20} />
                Reset
              </button>
            </div>
          </div>

          {/* Enhanced Track Visualization */}
          <div className="relative bg-gradient-to-b from-green-100 to-green-200 p-8 rounded-xl border-2 border-green-300">
            <div className="relative">
              {/* Enhanced Track with realistic appearance */}
              <div className="relative w-full h-8 mb-12">
                {/* Track bed */}
                <div className="w-full h-6 bg-gray-600 rounded-lg"></div>
                {/* Rails */}
                <div className="absolute top-1 left-0 w-full h-1 bg-gray-800 rounded-full"></div>
                <div className="absolute bottom-1 left-0 w-full h-1 bg-gray-800 rounded-full"></div>
                {/* Railroad ties */}
                {[...Array(15)].map((_, i) => (
                  <div
                    key={i}
                    className="absolute top-0 w-2 h-6 bg-amber-800"
                    style={{ left: `${i * 6.67}%` }}
                  />
                ))}
              </div>

              {/* Distance markers */}
              <div className="flex justify-between text-sm text-gray-700 mb-6 font-mono">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="text-center">
                    <div className="w-px h-4 bg-gray-400 mx-auto mb-1"></div>
                    <span>{Math.round((i * maxDistance) / 7)} mi</span>
                  </div>
                ))}
              </div>

              {/* Enhanced Trains with sliding animation */}
              <div className="relative h-24">
                {/* Train A with smooth sliding */}
                <div
                  className="absolute transition-all duration-100 ease-linear transform -translate-y-16"
                  style={{ 
                    left: `${trainAPos}px`,
                    transform: `translateX(${trainAPos}px) translateY(-64px)`
                  }}
                >
                  <div className="flex items-center">
                    <div className="relative">
                      {/* Train body */}
                      <div className="w-16 h-10 bg-gradient-to-r from-red-500 to-red-600 rounded-lg shadow-lg flex items-center justify-center border-2 border-red-700">
                        <span className="text-white font-bold text-lg">A</span>
                      </div>
                      {/* Smoke effect */}
                      <div className="absolute -top-2 left-2 text-gray-400 animate-pulse">💨</div>
                      {/* Wheels */}
                      <div className="absolute -bottom-1 left-1 w-3 h-3 bg-gray-800 rounded-full"></div>
                      <div className="absolute -bottom-1 right-1 w-3 h-3 bg-gray-800 rounded-full"></div>
                    </div>
                    <div className="ml-3 bg-white p-2 rounded-lg shadow-md">
                      <div className="font-bold text-red-600">Train A</div>
                      <div className="text-sm text-gray-600">{trainASpeed} mph</div>
                      <div className="text-xs text-gray-500">{trainADistance.toFixed(1)} mi</div>
                    </div>
                  </div>
                </div>

                {/* Train B with smooth sliding */}
                <div
                  className="absolute transition-all duration-100 ease-linear transform translate-y-6"
                  style={{ 
                    left: `${trainBPos}px`,
                    transform: scenario === 'opposite-direction' 
                      ? `translateX(${trainBPos}px) translateY(24px) scaleX(-1)` 
                      : `translateX(${trainBPos}px) translateY(24px)`
                  }}
                >
                  <div className="flex items-center">
                    <div className="relative">
                      {/* Train body */}
                      <div className="w-16 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg flex items-center justify-center border-2 border-blue-700">
                        <span className="text-white font-bold text-lg">B</span>
                      </div>
                      {/* Smoke effect */}
                      <div className="absolute -top-2 left-2 text-gray-400 animate-pulse">💨</div>
                      {/* Wheels */}
                      <div className="absolute -bottom-1 left-1 w-3 h-3 bg-gray-800 rounded-full"></div>
                      <div className="absolute -bottom-1 right-1 w-3 h-3 bg-gray-800 rounded-full"></div>
                    </div>
                    <div className={`ml-3 bg-white p-2 rounded-lg shadow-md ${scenario === 'opposite-direction' ? 'scale-x-[-1]' : ''}`}>
                      <div className="font-bold text-blue-600">Train B</div>
                      <div className="text-sm text-gray-600">{trainBSpeed} mph</div>
                      <div className="text-xs text-gray-500">{trainBDistance.toFixed(1)} mi</div>
                    </div>
                  </div>
                </div>

                {/* Meeting point indicator with animation */}
                {meeting && (
                  <div
                    className="absolute top-0 w-2 h-24 bg-gradient-to-b from-green-400 to-green-600 animate-pulse"
                    style={{ left: `${(meeting.distance / maxDistance) * 700}px` }}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg">
                      🎯 MEET
                    </div>
                    <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs bg-white px-2 py-1 rounded border">
                      {meeting.distance.toFixed(1)}mi
                    </div>
                  </div>
                )}
              </div>

              {/* Enhanced Time display with calculations */}
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
                        {scenario === 'same-direction' ? 'Relative Speed (mph)' : 'Combined Speed (mph)'}
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Calculator Toggle */}
        <div className="bg-white rounded-xl shadow-xl p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <Calculator className="text-indigo-600" />
              Complete Mathematical Solution
            </h2>
            <button
              onClick={() => setShowCalculations(!showCalculations)}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-lg hover:from-indigo-700 hover:to-indigo-800 transition-all shadow-lg"
            >
              <Calculator size={20} />
              {showCalculations ? 'Hide' : 'Show'} Full Calculations
            </button>
          </div>

          {showCalculations && meeting && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl border-2 border-gray-200">
                <h3 className="font-bold text-xl mb-4 text-gray-800">📋 Problem Setup:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg">
                  <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                    <strong>🚂 Train A:</strong> {trainASpeed} mph, {headStart}-hour head start
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <strong>🚂 Train B:</strong> {trainBSpeed} mph, {scenario === 'same-direction' ? 'same direction' : 'opposite direction'}
                  </div>
                </div>
              </div>

              {scenario === 'same-direction' ? (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border-2 border-blue-200">
                  <h3 className="font-bold text-xl mb-4 text-blue-800">🎯 Same Direction Solution:</h3>
                  <div className="space-y-4">
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 1:</strong> Let t = time Train B travels</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 2:</strong> Set up distance equations:</p>
                      <div className="ml-4 mt-2 font-mono text-blue-700">
                        <p>Train A distance = {trainASpeed}(t + {headStart})</p>
                        <p>Train B distance = {trainBSpeed}t</p>
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 3:</strong> Set distances equal (they meet when distances are equal):</p>
                      <div className="ml-4 mt-2 font-mono text-blue-700 text-xl">
                        {trainASpeed}(t + {headStart}) = {trainBSpeed}t
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-lg"><strong>Step 4:</strong> Solve for t:</p>
                      <div className="ml-4 mt-2 font-mono text-blue-700">
                        <p>{trainASpeed}t + {trainASpeed * headStart} = {trainBSpeed}t</p>
                        <p>{trainASpeed * headStart} = {trainBSpeed}t - {trainASpeed}t</p>
                        <p>{trainASpeed * headStart} = {trainBSpeed - trainASpeed}t</p>
                        <p className="text-xl font-bold">t = {trainASpeed * headStart} ÷ {trainBSpeed - trainASpeed} = {meeting.time.toFixed(2)} hours</p>
                      </div>
                    </div>
                    <div className="bg-green-100 p-4 rounded-lg border-2 border-green-300">
                      <p className="text-lg font-bold text-green-800">
                        ✅ Answer: Train B catches Train A after <span className="text-2xl">{meeting.time.toFixed(1)} hours</span>
                      </p>
                      <p className="text-green-700">Meeting distance: {meeting.distance.toFixed(1)} miles from start</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl border-2 border-purple-200">
                  <h3 className="font
