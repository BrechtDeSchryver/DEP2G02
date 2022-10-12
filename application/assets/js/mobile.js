const getMobileOS = () => {
    const ua = navigator.userAgent
    if (/android/i.test(ua)) {
      return "Android"
    }
    else if ((/iPad|iPhone|iPod/.test(ua)) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)){
      return "iOS"
    }
    return "Other"
  }

  const os = getMobileOS()

  if (os == "iOS"){
      document.getElementById("ioslink").style.display = "inline"
  } else {document.getElementById("ioslink").style.display = "none"}

