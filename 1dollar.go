package main

import (
  "fmt"
  "time"
  "sort"
  "math/rand"
)

func sum(a[]int)int {
  s := 0
  for i := 0; i < len(a); i++ {
    s += a[i]
  }
  return s
}

func main() {
  const N = 100
  const Cycles = 100
  rand.Seed(time.Now().UnixNano())
  for i := 1; i < 1000; i++ {
    p := make([]int, N, N)
    for i := 0; i < N; i++ {
      p[i] = N
    }
    for j := 0; j < i * Cycles; j++ {
      for k := 0; k < N; k++ {
        if p[k] > 0 {
          var to int
          for true {
            to = rand.Intn(N)
            if to != k { break }
          }
          p[k]--
          p[to]++
        }
      }
    }
    sort.Ints(p)
    pmin := p[0]
    pmax := p[N-1]
    median := p[N/2]
    q1 := float32(sum(p[0:N/4])) * 4 / float32(N)
    q3 := float32(sum(p[3*N/4:N])) * 4 / float32(N)
    fmt.Println(
      fmt.Sprintf("n = %6d => min/max/Δ/Md/Q1/Q3: %5d %5d %5d %5d %6.1f %6.1f",
        i * Cycles, pmin, pmax, pmax - pmin, median, q1, q3))
  }
}
