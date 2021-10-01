# <font color="crimson">Syllogistic Logics with ‘More Than’ and ‘Most’</font>



<div style="page-break-after: always;"></div>

## <font color="crimson">The Natural Logic Program</font>

- Aristotle, Van Benthem, Moss

- Natural language inference

  - No translating into FOL

- Special-purpose _logic engineering_

  - Complete _and decidable_ logics
  - 5 different systems in this talk alone!


<div style="page-break-after: always;"></div>

## <font color="crimson">Logics about Size Comparison</font>

- Restricted domain: _Reasoning about sizes_
- Why not embed into FOL with Arithmetic?
  - Decidable $\to$ More cognitively plausible
  - Light $\to$ More cognitively plausible
  - Counting is not needed:
    - “There is more sand than water in the pond”





<div style="page-break-after: always;"></div>

## <font color="red">$\mathcal{S(card)}$:</font> <font color="crimson">Syllogistic + ‘More Than’ + ‘At Least as Many’</font>

- $a, b, c, ...$ are <font color="red">nouns</font>

- $all(a, b)$
- $some(a, b)$
- $more(a, b)$
- $atLeast(a, b)$



- _No connectives $\and, \or \neg$_

- _No quantifiers $\forall, \exists$_





<div style="page-break-after: always;"></div>

## <font color="red">$\mathcal{S(card)}$:</font> <font color="crimson">Semantics</font>

- Models: $\mathcal{M}$ consisting of set $M$.
- For all nouns $a$, $[\![a]\!] \sube M$



- $\mathcal{M} \vDash all(a, b)$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iff   $[\![a]\!] \sube [\![b]\!]$
- $\mathcal{M} \vDash some(a, b)$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iff   $[\![a]\!] \cap [\![b]\!] \ne \empty$
- $\mathcal{M} \vDash more(a, b)$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iff   $|[\![a]\!]| \gt |[\![b]\!]|$
- $\mathcal{M} \vDash atLeast(a, b)$&nbsp;&nbsp;&nbsp;iff   $|[\![a]\!]| \ge |[\![b]\!]|$



- $\Gamma \vDash \varphi$ iff every **FINITE** model $\mathcal{M}$ which satisfies $\Gamma$ satisfies $\varphi$.





<div style="page-break-after: always;"></div>

## <font color="red">$\mathcal{S(card)}$:</font> <font color="crimson">Natural Deduction Rules</font>

**See board**



<div style="page-break-after: always;"></div>

## <font color="red">$\mathcal{S(card)}$:</font> <font color="crimson">Completeness Theorem</font>

<font color="crimson">**Theorem:**</font> $\mathcal{S(card)}$ is complete, i.e. $\Gamma \vDash \varphi$ iff $\Gamma \vdash \varphi$.



- From Larry Moss’ “Syllogistic Logic with Cardinality Comparisons”



<div style="page-break-after: always;"></div>

## <font color="orange">$\mathcal{S^\dagger(card)}$:</font>  <font color="crimson">$\mathcal{S(card)}$ + Noun Complement</font>

- For a noun $a$, we allow $a$ to be complemented: $\bar a$
- $\bar{\bar{a}} = a$ _at syntax level_
- **Semantics:** $[\![\bar a]\!] = M \setminus [\![a]\!]$
- **Rules of Inference:**
  - **See board**





<div style="page-break-after: always;"></div>

## <font color="orange">$\mathcal{S^\dagger(card)}$:</font> <font color="crimson">Completeness Theorem</font>

<font color="crimson">**Theorem:**</font> $\mathcal{S^{\dagger}(card)}$ is complete, i.e. $\Gamma \vDash \varphi$ iff $\Gamma \vdash \varphi$.

- More complicated than the proof for $\mathcal{S(card)}$!



<font color="crimson">**Bonus Theorem:**</font> $\mathcal{S^{\dagger}(card)}$ is decidable in polynomial time!



<div style="page-break-after: always;"></div>

## <font color="green">$\mathcal{S(most)}$:</font> <font color="crimson">Syllogistic + ‘Most’</font>

- $all(a, b)$
- $some(a, b)$
- $most(a, b)$



- $\mathcal{M} \vDash most(a, b)$             iff   $|[\![a]\!] \cap [\![b]\!]| \gt \dfrac{1}{2}[\![a]\!]$



<div style="page-break-after: always;"></div>

## <font color="green">$\mathcal{S(most)}$:</font> <font color="crimson">Natural Deduction Rules</font>

**See board**



<font color="crimson">**Theorem:**</font> $\mathcal{S(most)}$ is complete. -- and decidable in polynomial time!



<div style="page-break-after: always;"></div>

## <font color="crimson">The Hierarchy of Syllogistic Logics</font>

$\mathcal{All}$

 &nbsp;$\big \downarrow$

$\mathcal{S}$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\to$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color="green">$\mathcal{S(most)}$</font>

 &nbsp;$\big \downarrow$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\big \downarrow$

<font color="red">$\mathcal{S(card)}$</font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\big \downarrow$

 &nbsp;$\big \downarrow$&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$\big \downarrow$

<font color="orange">$\mathcal{S^{\dagger}(card)}$</font> $\to$ <font color="purple">**Holy Grail**</font>



- We want a complete logic involving ‘more than’ _and_ ‘most’

- Can’t just combine rules, because of interplay between ‘more than’ and ‘most’



<div style="page-break-after: always;"></div>

## <font color="crimson">A Solution: Complement _and Intersection_</font>

- $$most(a, b) \equiv more(a \cap b, a \cap \bar b)$$



- So we need **noun complement** _and_ **noun intersection**

- It is easier to make rules for Union $\cup$
  - $a \cap b \equiv \overline{\bar a \cap \bar b}$



<div style="page-break-after: always;"></div>

## <font color="blue">$\mathcal{S^{\cup}(card)}$:</font> <font color="crimson">$\mathcal{S(card)}$ + Noun Union</font>

- For _base_ nouns $a, b$, we allow $a$ and $b$ to be unioned: $$a \cup b$$
- We assume laws of boolean algebra at _syntax level_ (?)
- **Semantics:** $$[\![a \cup b]\!] = [\![a]\!] \cup [\![b]\!]$$
- **Rules of Inference:**
  - **See board**



<font color="crimson">**Conjecture:**</font> The set of rules given above for $\mathcal{S^{\cup}(card)}$ is complete.



<div style="page-break-after: always;"></div>

## <font color="purple">$\mathcal{S^{\dagger \cup}(card)}$:</font> <font color="crimson">$\mathcal{S(card)}$ + Noun Union + Noun Complement</font>

- The Holy Grail!
- What is a complete set of rules?
  - Can’t just haphazardly combine $\mathcal{S^{\dagger}(card)}$ and $\mathcal{S^{\cup}(card)}$



<div style="page-break-after: always;"></div>

## <font color="purple">$\mathcal{S^{\dagger \cup}(card)}$:</font> <font color="crimson">Proposed Rules</font>

**See board**



- We can derive the first 6 ‘most’ rules already!
  - Remember that infinite schema!



